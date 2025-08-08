import os

from dotenv import load_dotenv

from ..db.sqlmodel_models import Shipment, ShipmentEvent, ShipmentStatus
from ..utils.token import generate_url_safe_token
from .o_base import BaseService
from .o_notification import NotificationService

load_dotenv()
APP_DOMAIN = os.getenv("APP_DOMAIN")


class ShipmentEventService(BaseService):
    def __init__(self, session, tasks):
        super().__init__(ShipmentEvent, session)
        self.notification_service = NotificationService(tasks)

    async def add(
        self,
        shipment: Shipment,
        location: int = None,
        status: ShipmentStatus = None,
        description: str = None,
    ) -> ShipmentEvent:

        last_event = await self.get_latest_event(shipment)
        if last_event:
            location = location if location else last_event.location
            status = status if status else last_event.status
        else:
            location = (
                location if location else shipment.destination
            )  # optional fallback
            status = status if status else ShipmentStatus.placed

        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=(
                description
                if description
                else self._generate_description(status, location)
            ),
            shipment_id=shipment.id,
        )

        await self._notify(shipment, status)

        return await self._add(new_event)

    async def get_latest_event(self, shipment: Shipment):
        """
        sorts timeline list in  ascending order by created_at
        """
        timeline = shipment.timeline
        if not timeline:
            return None  # or raise a custom exception if this is unexpected
        timeline.sort(key=lambda event: event.created_at)
        return timeline[-1]

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.delivered:
                return "successfully delivered"
            case ShipmentStatus.cancelled:
                return "cancelled by seller"
            case _:  # and ShipmentStatus is : in_transit
                return f"scanned at {location}"

    async def _notify(self, shipment: Shipment, status: ShipmentStatus):

        if status == ShipmentStatus.in_transit:
            return

        subject: str
        context = {}
        template_name: str

        match status:
            case ShipmentStatus.placed:
                subject = "Your Order is Shipped 🚛"
                context["seller"] = shipment.seller.name
                context["id"] = shipment.id
                context["partner"] = shipment.delivery_partner.name
                template_name = "email/mail_placed.html"

            case ShipmentStatus.out_for_delivery:
                subject = "Your Order is Arriving Soon 🛵"
                context["id"] = shipment.id
                template_name = "email/mail_out_for_delivery.html"

            case ShipmentStatus.delivered:
                subject = "Your Order is Delivered ✅"
                token = generate_url_safe_token({"id": str(shipment.id)})
                context["id"] = shipment.id
                context["seller"] = shipment.seller.name
                context["review_url"] = (
                    f"http://{APP_DOMAIN}/shipmentv3/review?token={token}"
                )
                template_name = "email/mail_delivered.html"

            case ShipmentStatus.cancelled:
                subject = "Your Order is Cancelled ❌"
                context["id"] = shipment.id
                template_name = "email/mail_cancelled.html"

        await self.notification_service.send_email_with_template(
            recipients=[shipment.client_contact_email],
            subject=subject,
            context=context,
            template_name=template_name,
        )
