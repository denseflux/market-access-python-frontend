import json
from operator import itemgetter

from barriers.constants import Statuses
from core.filecache import memfiles
from utils.exceptions import HawkException

from django.conf import settings
from mohawk import Sender
import redis
import requests


redis_client = None
if not settings.MOCK_METADATA:
    redis_client = redis.Redis.from_url(url=settings.REDIS_URI)


def get_metadata():
    if settings.MOCK_METADATA:
        file = f"{settings.BASE_DIR}/../core/fixtures/metadata.json"
        return Metadata(json.loads(memfiles.open(file)))
    else:
        metadata = redis_client.get("metadata")
        if metadata:
            return Metadata(json.loads(metadata))

    url = f"{settings.MARKET_ACCESS_API_URI}metadata"
    credentials = {
        "id": settings.MARKET_ACCESS_API_HAWK_ID,
        "key": settings.MARKET_ACCESS_API_HAWK_KEY,
        "algorithm": "sha256",
    }
    sender = Sender(
        credentials,
        url,
        "GET",
        content="",
        content_type="text/plain",
        always_hash_content=False,
    )

    response = requests.get(
        url,
        verify=not settings.DEBUG,
        headers={"Authorization": sender.request_header, "Content-Type": "text/plain",},
    )

    if response.ok:
        metadata = response.json()
        redis_client.set(
            "metadata", json.dumps(metadata), ex=settings.METADATA_CACHE_TIME
        )
        return Metadata(metadata)

    raise HawkException("Call to fetch metadata failed")


class Metadata:
    """
    Wrapper around the raw metadata with helper functions
    """

    STATUS_INFO = {
        Statuses.UNFINISHED: {
            "name": "Unfinished",
            "modifier": "unfinished",
            "hint": "Barrier is unfinished",
        },
        Statuses.OPEN_PENDING_ACTION: {
            "name": "Pending",
            "modifier": "open-pending-action",
            "hint": "Barrier is awaiting action",
        },
        Statuses.OPEN_IN_PROGRESS: {
            "name": "Open",
            "modifier": "open-in-progress",
            "hint": "Barrier is being worked on",
        },
        Statuses.RESOLVED_IN_PART: {
            "name": "Part resolved",
            "modifier": "resolved",
            "hint": (
                "Barrier impact has been significantly reduced but remains " "in part"
            ),
        },
        Statuses.RESOLVED_IN_FULL: {
            "name": "Resolved",
            "modifier": "resolved",
            "hint": "Barrier has been resolved for all UK companies",
        },
        Statuses.DORMANT: {
            "name": "Paused",
            "modifier": "hibernated",
            "hint": "Barrier is present but not being pursued",
        },
        Statuses.ARCHIVED: {
            "name": "Archived",
            "modifier": "archived",
            "hint": "Barrier is archived",
        },
        Statuses.UNKNOWN: {
            "name": "Unknown",
            "modifier": "unknown",
            "hint": "Barrier requires further work for the status to be known",
        },
    }

    def __init__(self, data):
        self.data = data

    def get_admin_area(self, admin_area_id):
        for admin_area in self.data["country_admin_areas"]:
            if admin_area["id"] == admin_area_id and admin_area["disabled_on"] is None:
                return admin_area

    def get_admin_areas(self, admin_area_ids):
        """
        Helper to get admin areas data in bulk.

        :param admin_area_ids: either a list or a comma separated string of UUIDs
        :return: GENERATOR - data of admin areas
        """
        area_ids = admin_area_ids or []
        if type(area_ids) == str:
            area_ids = admin_area_ids.replace(" ", "").split(",")
        admin_areas = [self.get_admin_area(area_id) for area_id in area_ids]
        return admin_areas

    def get_admin_areas_by_country(self, country_id):
        return [
            admin_area
            for admin_area in self.data["country_admin_areas"]
            if admin_area["country"]["id"] == country_id
        ]

    def get_country(self, country_id):
        for country in self.data["countries"]:
            if country["id"] == country_id:
                return country

    def get_country_list(self):
        return self.data["countries"]

    def get_location_text(self, country_id, admin_area_ids):
        country_data = self.get_country(country_id)

        if country_data:
            country_name = country_data["name"]
        else:
            country_name = ""

        if admin_area_ids:
            admin_areas_string = ", ".join(
                [
                    self.get_admin_area(admin_area_id)["name"]
                    for admin_area_id in admin_area_ids
                ]
            )
            return f"{admin_areas_string} ({country_name})"

        return country_name

    def get_overseas_region_list(self):
        regions = {
            country["overseas_region"]["id"]: country["overseas_region"]
            for country in self.get_country_list()
            if country["disabled_on"] is None
            and country.get("overseas_region") is not None
        }
        regions = list(regions.values())
        regions.sort(key=itemgetter("name"))
        return regions

    def get_sector(self, sector_id):
        for sector in self.data.get("sectors", []):
            if sector["id"] == sector_id:
                return sector

    def get_sectors(self, sector_ids):
        """
        Helper to get sectors data in bulk.

        :param sector_ids: either a list or a comma separated string of UUIDs
        :return: GENERATOR - data of sectors
        """
        sec_ids = sector_ids or []
        if type(sec_ids) == str:
            sec_ids = sector_ids.replace(" ", "").split(",")
        sectors = (self.get_sector(sector_id) for sector_id in sec_ids)
        return sectors

    def get_sectors_by_ids(self, sector_ids):
        return [
            sector
            for sector in self.data.get("sectors", [])
            if sector["id"] in sector_ids and sector["disabled_on"] is None
        ]

    def get_sector_list(self, level=None):
        return [
            sector
            for sector in self.data["sectors"]
            if (level is None or sector["level"] == level)
            and sector["disabled_on"] is None
        ]

    def get_status(self, status_id):
        for id, name in self.data["barrier_status"].items():
            self.STATUS_INFO[id]["id"] = id
            self.STATUS_INFO[id]["name"] = name

        return self.STATUS_INFO[status_id]

    def get_status_text(
        self, status_id, sub_status=None, sub_status_other=None,
    ):
        if status_id in self.STATUS_INFO.keys():
            name = self.get_status(status_id)["name"]
            if sub_status and status_id == Statuses.OPEN_PENDING_ACTION:
                sub_status_text = self.get_sub_status_text(
                    sub_status, sub_status_other,
                )
                return f"{name} ({sub_status_text})"
            return name

        return status_id

    def get_sub_status_text(self, sub_status, sub_status_other=None):
        if sub_status == "OTHER":
            return sub_status_other

        return self.data["barrier_pending"].get(sub_status)

    def get_problem_status(self, problem_status_id):
        status_types = self.data["status_types"]
        status_types.update(
            {
                "1": "A procedural, short-term barrier",
                "2": "A long-term strategic barrier",
            }
        )
        return status_types.get(str(problem_status_id))

    def get_source(self, source):
        return self.data["barrier_source"].get(source)

    def get_priority(self, priority_code):
        if priority_code == "None":
            priority_code = "UNKNOWN"

        for priority in self.data["barrier_priorities"]:
            if priority["code"] == priority_code:
                return priority

    def get_assessment_name(self, assessment_code):
        assessment_names = {
            "impact": "Economic assessment",
            "value_to_economy": "Value to UK Economy",
            "import_market_size": "Import Market Size",
            "export_value": "Value of currently affected UK exports",
            "commercial_value": "Commercial Value",
        }
        return assessment_names.get(assessment_code)

    def get_category_list(self, sort=True):
        """
        Dedupe and sort the barrier types
        """
        ids = []
        unique_categories = []
        for category in self.data.get("categories"):
            if category["id"] not in ids:
                unique_categories.append(category)
                ids.append(category["id"])

        if sort:
            unique_categories.sort(key=itemgetter("title"))
        return unique_categories

    def get_category(self, category_id):
        for category in self.data["categories"]:
            if str(category["id"]) == str(category_id):
                return category

    def get_categories_by_group(self, group):
        return [
            barrier_type
            for barrier_type in self.get_category_list(sort=False)
            if barrier_type["category"] == group
        ]

    def get_goods(self):
        return self.get_categories_by_group("GOODS")

    def get_services(self):
        return self.get_categories_by_group("SERVICES")

    def get_impact_text(self, impact_code):
        return self.data.get("assessment_impact", {}).get(impact_code)

    def get_report_stages(self):
        stages = self.data.get("report_stages", {})
        # filter out "Add a barrier" as that's not a valid stage
        exclude_stages = ("Add a barrier",)
        remove_keys = []
        for key, value in stages.items():
            if value in exclude_stages:
                remove_keys.append(key)

        for key in remove_keys:
            stages.pop(key)

        return stages

    def get_barrier_tag(self, tag_id):
        for tag in self.get_barrier_tags():
            if str(tag["id"]) == str(tag_id):
                return tag

    def get_barrier_tags(self):
        tags = self.data.get("barrier_tags", [])
        return sorted(tags, key=lambda k: k['order'])

    def get_barrier_tag_choices(self):
        """
        Generates tag choices.
        Includes all tags that are available.
        """
        return (
            (tag["id"], tag["title"], tag["description"])
            for tag in self.get_barrier_tags()
        )

    def get_report_tag_choices(self):
        """
        Generates tag choices.
        Only returns a subset of tags when reporting a barrier.
        """
        return (
            (tag["id"], tag["title"], tag["description"])
            for tag in self.get_barrier_tags()
            if tag["show_at_reporting"] is True
        )

    def get_trade_direction(self, key=None, all_items=False):
        """
        Helper to get either a value or all items for trade_direction.

        :param key:         STR  - dict key
        :param all_items:   BOOL
        :return: Returns either all items in the dict or the value of a specific key
        """
        trade_directions = self.data.get("trade_direction", {})
        if all_items:
            return trade_directions.items()
        else:
            return trade_directions.get(key)

    def get_trade_direction_choices(self):
        return (td for td in self.get_trade_direction(all_items=True))

    def get_wto_committee_groups(self):
        return self.data.get("wto_committee_groups", [])
