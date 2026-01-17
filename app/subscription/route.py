from fastapi import APIRouter, Request
from app.subscription.webhook import handle_stripe_webhook
from app.core.annotations import TransactionSession

router = APIRouter(tags=["subscriptions"])


@router.post("/webhook", operation_id="stripeWebhook")
async def stripe_webhook(request: Request, session: TransactionSession):
    print("Stripe webhook received")
    return await handle_stripe_webhook(request, session)
