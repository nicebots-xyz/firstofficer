import hikari
import yuyo
import os

from datetime import datetime

from fligthPlanGetter import fetch_popular_flight_plans
from imgPlotter import create_geo_image
from config import component_client


async def flightplan(ctx: hikari.CommandInteraction):
    from_airport: str = ctx.options[0].value
    to_airport: str = ctx.options[1].value
    embeds: list[tuple[int, tuple[hikari.Embed, hikari.File]]] = []
    ifr_routes = await fetch_popular_flight_plans(from_airport, to_airport)
    if isinstance(ifr_routes, str):
        await ctx.edit_initial_response(content=ifr_routes)

    embeds = []
    files = []
    os.makedirs("images", exist_ok=True)
    for i, route in enumerate(ifr_routes):
        embed = hikari.Embed(
            title=f"Flight Plan {i+1} of {len(ifr_routes)}",
            description=route["notes"],
            color=hikari.Color.from_hex_code("#0000FF"),
        )
        valueasy = " ".join([f"{node['ident']}" for node in route["nodes"]])
        img_buffer = create_geo_image(route["nodes"])
        filename = f"./images/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
        with open(filename, "wb") as f:
            f.write(img_buffer.getvalue())
        file = hikari.File(filename)
        files.append(filename)
        embed.set_image(file)
        embed.add_field(name="Fixes", value=f"```\n{valueasy}\n```")
        embeds.append(embed)
    paginatorIter = iter([(hikari.UNDEFINED, element) for element in embeds])
    paginator = (
        yuyo.ComponentPaginator(
            paginatorIter,
            triggers=[],
        )
        .add_first_button(
            style=hikari.ButtonStyle.PRIMARY, emoji=hikari.UNDEFINED, label="<<"
        )
        .add_previous_button(
            style=hikari.ButtonStyle.DANGER, emoji=hikari.UNDEFINED, label="<"
        )
        .add_next_button(
            style=hikari.ButtonStyle.SUCCESS, emoji=hikari.UNDEFINED, label=">"
        )
        .add_last_button(
            style=hikari.ButtonStyle.PRIMARY, emoji=hikari.UNDEFINED, label=">>"
        )
    )
    first_page = await paginator.get_next_entry()
    assert (
        first_page
    ), "get_next_entry shouldn't ever return None here as we already know the amount of pages"
    message = await ctx.edit_initial_response(
        **first_page.to_kwargs(), components=paginator.rows
    )
    component_client.register_executor(paginator, message=message)

commands = {
    "flightplan": flightplan,
}


async def unknown_command(interaction: hikari.CommandInteraction):
    await interaction.respond("Unknown command")


# This function will handle the interactions received
async def handle_command(interaction: hikari.CommandInteraction):
    # Create an initial response to be able to take longer to respond
    yield interaction.build_deferred_response()
    cmd = commands.get(interaction.command_name, unknown_command)
    await cmd(interaction)
