import logging
import inngest


inngest_client = inngest.Inngest(app_id="frezume_svc", logger=logging.getLogger("uvicorn"))


@inngest_client.create_function(fn_id="func", trigger=inngest.TriggerEvent(event="app/func"))
async def inngest_function(ctx: inngest.Context) -> str:
    ctx.logger.info(ctx.event)
    return "done"
