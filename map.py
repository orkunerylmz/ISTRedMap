import folium
import pandas as pd
from itertools import cycle
from folium.plugins import HeatMap, MarkerCluster, MiniMap


data = pd.read_csv("cleaned_data.csv").sample(10)

m = folium.Map(location=[41.0082, 28.9784], zoom_start=11)

heat_data = data[['LATITUDE', 'LONGITUDE']]
HeatMap(heat_data.values, radius=10).add_to(m)

marker_cluster = MarkerCluster().add_to(m)

data['YEAR'] = data['ANNOUNCEMENT_STARTING_DATETIME'].str[:4]
unique_years = sorted(data['YEAR'].unique())

available_colors = [
    'red', 'green', 'blue', 'purple', 'orange',
    'darkred', 'darkgreen', 'cadetblue', 'black',
    'lightblue', 'lightgreen', 'beige', 'gray', 'darkpurple'
]
color_cycle = cycle(available_colors)
year_color_map = {year: next(color_cycle) for year in unique_years}

for _, row in data.iterrows():
    title = row['ANNOUNCEMENT_TITLE']
    datetime = row['ANNOUNCEMENT_STARTING_DATETIME']
    tarih, saat = datetime.split(" ")
    year = tarih[:4]

    popup_html = f"""
    <b>🗂️ Başlık:</b> {title}<br>
    <b>🕒 Saat:</b> {saat}<br>
    <b>📅 Tarih:</b> {tarih}
    """
    popup = folium.Popup(popup_html, max_width=300, min_width=200)
    color = year_color_map.get(year, 'gray')

    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=popup,
        tooltip=title,
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster)

MiniMap(toggle_display=True).add_to(m)

legend_html = """
<div id="legend-toggle" style="
     position: fixed;
     bottom: 30px; left: 30px;
     z-index:9998;
     background-color: #ffffff;
     border: 1px solid #888;
     border-radius: 5px;
     padding: 5px 10px;
     cursor: pointer;
     font-weight: bold;
     box-shadow: 0 0 5px rgba(0,0,0,0.3);
">🎨 Renk Açıklaması</div>

<div id="legend-content" style="
     position: fixed; 
     bottom: 70px; left: 30px; 
     z-index:9999;
     font-size:14px;
     background-color: rgba(255,255,255,0.95);
     padding: 10px 15px;
     border-radius: 8px;
     box-shadow: 0 0 5px rgba(0,0,0,0.4);
     display: none;
">
<b>🗓️ Yıllara Göre Renkler:</b><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 5px;">
"""

for year, color in year_color_map.items():
    legend_html += f"""
    <div style="display: flex; align-items: center; gap: 5px;">
        <i style="background:{color}; width:15px; height:15px; display:inline-block; border:1px solid #000;"></i>
        {year}
    </div>
    """

legend_html += """
</div>
</div>

<script>
document.getElementById('legend-toggle').onclick = function() {
    var content = document.getElementById('legend-content');
    content.style.display = (content.style.display === 'none') ? 'block' : 'none';
};
</script>
"""

m.get_root().html.add_child(folium.Element(legend_html))

m.save("ist_map.html")
print("📌 Map with collapsible legend created: ist_map.html")



