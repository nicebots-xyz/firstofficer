import hikari

from config import component_client


async def create_commands(bot: hikari.RESTBot):
    component_client.open()
    application = await bot.rest.fetch_application()

    flightplan = bot.rest.slash_command_builder(
        "flightplan", "Get a flight plan from Flight Plan Database"
    )
    from_airport = hikari.CommandOption(
        type=hikari.OptionType.STRING,
        name="from_airport",
        description="The departure airport",
        is_required=True,
        min_length=4,
        max_length=4,
    )

    to_airport = hikari.CommandOption(
        type=hikari.OptionType.STRING,
        name="to_airport",
        description="The arrival airport",
        is_required=True,
        min_length=4,
        max_length=4,
    )

    flightplan.add_option(from_airport).add_option(to_airport)

    await bot.rest.set_application_commands(
        application=application.id,
        commands=[
            flightplan,
        ],
    )
