import plotly.graph_objects as go
import io
from PIL import Image


def create_geo_image(flight_path, scale_factor=2, margin=0.5):
    # Create the figure
    fig = go.Figure()

    all_lats = []
    all_lons = []

    # Add lines
    lats = [point["lat"] for point in flight_path]
    lons = [point["lon"] for point in flight_path]

    all_lats.extend(lats)
    all_lons.extend(lons)

    fig.add_trace(
        go.Scattergeo(
            lat=lats,
            lon=lons,
            mode="lines",
            line=dict(width=2, color="blue"),
            # disable the legend
            showlegend=False,
        )
    )

    min_lat, max_lat = min(all_lats), max(all_lats)
    min_lon, max_lon = min(all_lons), max(all_lons)
    # calculate the top margin + based on the lat and lon, cause at the top we have the arced pahs
    top_margin = (max_lat - min_lat) * 0.1
    # Add some margins for better visibility
    min_lat -= margin
    max_lat += margin + top_margin
    min_lon -= margin
    max_lon += margin

    # Layout properties

    fig.update_geos(
        projection_type="equirectangular",
        lataxis_range=[min_lat, max_lat],
        lonaxis_range=[min_lon, max_lon],
        showland=True,
        landcolor="rgb(243, 243, 243)",
        showocean=True,
        oceancolor="rgb(127,205,255)",
        showcountries=True,
        countrycolor="Black",
        countrywidth=0.5,
        showlakes=True,
        lakecolor="Blue",
    )

    fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=0, pad=0))
    # Convert the figure to a PNG image
    img_bytes = fig.to_image(format="png", scale=scale_factor)

    # Create a BytesIO object and save the PNG image data to it
    buf = io.BytesIO()
    buf.write(img_bytes)
    buf.seek(0)

    return buf
