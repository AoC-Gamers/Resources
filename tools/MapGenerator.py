import csv
import json
import random
import os
import argparse

# ========= Maplist embebido ========= #
maplist_default = """Codigo,Campaña,Capitulo,Origen
c1m1_hotel,Dead Center,The Hotel,Oficial
c1m2_streets,Dead Center,The Streets,Oficial
c1m3_mall,Dead Center,The Mall,Oficial
c1m4_atrium,Dead Center,Atrium Finale,Oficial
c2m1_highway,Dark Carnival,The Highway,Oficial
c2m2_fairgrounds,Dark Carnival,The Fairgrounds,Oficial
c2m3_coaster,Dark Carnival,The Coaster,Oficial
c2m4_barns,Dark Carnival,The Barns,Oficial
c2m5_concert,Dark Carnival,The Concert,Oficial
c3m1_plankcountry,Swamp Fever,Plank Country,Oficial
c3m2_swamp,Swamp Fever,The Swamp,Oficial
c3m3_shantytown,Swamp Fever,Shanty Town,Oficial
c3m4_plantation,Swamp Fever,The Plantation,Oficial
c4m1_milltown_a,Hard Rain,The Milltown,Oficial
c4m2_sugarmill_a,Hard Rain,The Sugar Mill,Oficial
c4m3_sugarmill_b,Hard Rain,Mill Escape,Oficial
c4m4_milltown_b,Hard Rain,Return to Town,Oficial
c4m5_milltown_escape,Hard Rain,Town Escape,Oficial
c5m1_waterfront,The Parish,The Waterfront,Oficial
c5m2_park,The Parish,The Park,Oficial
c5m3_cemetery,The Parish,The Cemetery,Oficial
c5m4_quarter,The Parish,The Quarter,Oficial
c5m5_bridge,The Parish,The Bridge,Oficial
c6m1_riverbank,The Passing,The Riverbank,Oficial
c6m2_bedlam,The Passing,The Underground,Oficial
c6m3_port,The Passing,The Port,Oficial
c7m1_docks,The Sacrifice,The Docks,Oficial
c7m2_barge,The Sacrifice,The Barge,Oficial
c7m3_port,The Sacrifice,Port Finale,Oficial
c8m1_apartment,No Mercy,The Apartments,Oficial
c8m2_subway,No Mercy,The Subway,Oficial
c8m3_sewers,No Mercy,The Sewer,Oficial
c8m4_interior,No Mercy,The Hospital,Oficial
c8m5_rooftop,No Mercy,Rooftop Finale,Oficial
c9m1_alleys,Crash Course,The Alleys,Oficial
c9m2_lots,Crash Course,The Truck Depot Finale,Oficial
c10m1_caves,Death Toll,The Turnpike,Oficial
c10m2_drainage,Death Toll,The Drains,Oficial
c10m3_ranchhouse,Death Toll,The Church,Oficial
c10m4_mainstreet,Death Toll,The Town,Oficial
c10m5_houseboat,Death Toll,Boathouse Finale,Oficial
c11m1_greenhouse,Dead Air,The Greenhouse,Oficial
c11m2_offices,Dead Air,The Crane,Oficial
c11m3_garage,Dead Air,The Construction Site,Oficial
c11m4_terminal,Dead Air,The Terminal,Oficial
c11m5_runway,Dead Air,Runway Finale,Oficial
c12m1_hilltop,Blood Harvest,The Woods,Oficial
c12m2_traintunnel,Blood Harvest,The Tunnel,Oficial
c12m3_bridge,Blood Harvest,The Bridge,Oficial
c12m4_barn,Blood Harvest,The Train Station,Oficial
c12m5_cornfield,Blood Harvest,Farmhouse Finale,Oficial
c13m1_alpinecreek,Cold Stream,Alpine Creek,Oficial
c13m2_southpinestream,Cold Stream,South Pine Stream,Oficial
c13m3_memorialbridge,Cold Stream,Memorial Bridge,Oficial
c13m4_cutthroatcreek,Cold Stream,Cut-throat Creek,Oficial
c14m1_junkyard,The Last Stand,The Junkyard,Oficial
c14m2_lighthouse,The Last Stand,Lighthouse Finale,Oficial
l4d2_city17_01,City 17,1: Tunnels,WorkShop
l4d2_city17_02,City 17,2: To the surface,WorkShop
l4d2_city17_03,City 17,3: Streets,WorkShop
l4d2_city17_04,City 17,4: Hospital,WorkShop
l4d2_city17_05,City 17,5: Trainstation,WorkShop
CCR1_alleys,Crash Course: ReRouted,Alleys,WorkShop
CCR2_lots,Crash Course: ReRouted,Lots,WorkShop
CCR3_Factories,Crash Course: ReRouted,Factories,WorkShop
CCR4_Waterworks,Crash Course: ReRouted,Waterworks,WorkShop
dkr_m1_motel,Dark Carnival Remix,The Motel,WorkShop
dkr_m2_carnival,Dark Carnival Remix,The Carnival,WorkShop
dkr_m3_tunneloflove,Dark Carnival Remix,The Tunnel of Love,WorkShop
dkr_m4_ferris,Dark Carnival Remix,The Ferris Wheel,WorkShop
dkr_m5_stadium,Dark Carnival Remix,The Stadium,WorkShop
l4d2_daybreak01_hotel,Daybreak,1: The Hotel,WorkShop
l4d2_daybreak02_coastline,Daybreak,2: The Coastline,WorkShop
l4d2_daybreak03_bridge,Daybreak,3: The Bridge,WorkShop
l4d2_daybreak04_cruise,Daybreak,4: The Outskirts,WorkShop
l4d2_daybreak05_rescue,Daybreak,5: Alcatraz Finale,WorkShop
l4d_dbd2dc_anna_is_gone,Dead Before Down,Anna is gone,WorkShop
l4d_dbd2dc_the_mall,Dead Before Down,The mall,WorkShop
l4d_dbd2dc_clean_up,Dead Before Down,Clean up,WorkShop
l4d_dbd2dc_undead_center,Dead Before Down,Undead center,WorkShop
l4d_dbd2dc_new_dawn,Dead Before Down,New dawn,WorkShop
cdta_01detour,Detour Ahead,DTA Versus,WorkShop
cdta_02road,Detour Ahead,DTA2 Versus,WorkShop
cdta_03warehouse,Detour Ahead,DTA3 Versus,WorkShop
cdta_04onarail,Detour Ahead,DTA4 Versus,WorkShop
cdta_05finalroad,Detour Ahead,DTA5 Final Road,WorkShop
l4d2_diescraper1_apartment_361,Diescraper Redux,Apartment complex,WorkShop
l4d2_diescraper2_streets_361,Diescraper Redux,Downtown military outpost,WorkShop
l4d2_diescraper3_mid_361,Diescraper Redux,The Skymall,WorkShop
l4d2_diescraper4_top_361,Diescraper Redux,The top suites,WorkShop
dprm1_milltown_a,Hard Rain Downpour,Chapter 1: Milltown,WorkShop
dprm2_sugarmill_a,Hard Rain Downpour,Chapter 2: Sugarmill,WorkShop
dprm3_sugarmill_b,Hard Rain Downpour,Chapter 3: Sugarmill Return,WorkShop
dprm4_milltown_b,Hard Rain Downpour,Chapter 4: Milltown Return,WorkShop
dprm5_milltown_escape,Hard Rain Downpour,Chapter 5: Milltown Escape,WorkShop
l4d2_ff01_woods,Fatal Freight,1: The Woods,WorkShop
l4d2_ff02_factory,Fatal Freight,2: The Factory,WorkShop
l4d2_ff03_highway,Fatal Freight,3: The Highway,WorkShop
l4d2_ff04_plant,Fatal Freight,4: The Plant,WorkShop
l4d2_ff05_station,Fatal Freight,5: Trainyard Finale,WorkShop
hf01_theforest,Haunted Forest,1: The Forest,WorkShop
hf02_thesteeple,Haunted Forest,2: The Steeple,WorkShop
hf03_themansion,Haunted Forest,3: The Mansion,WorkShop
hf04_escape,Haunted Forest,4: The Tunnel,WorkShop
l4d_ihm01_forest,I hate Mountains,1: Lost in the Woods,WorkShop
l4d_ihm02_manor,I hate Mountains,2: Climbing the Manor,WorkShop
l4d_ihm03_underground,I hate Mountains,3: The Underground Way,WorkShop
l4d_ihm04_lumberyard,I hate Mountains,4: Lumberyard Evacuation,WorkShop
l4d_ihm05_lakeside,I hate Mountains,5: Lakeside Finale,WorkShop
nmrm1_apartment,No mercy Rehab,The Apartments,WorkShop
nmrm2_subway,No mercy Rehab,The Subway,WorkShop
nmrm3_sewers,No mercy Rehab,The Sewer,WorkShop
nmrm4_hospital,No mercy Rehab,The Hospital,WorkShop
nmrm5_rooftop,No mercy Rehab,Rooftop Finale,WorkShop
x1m1_cliffs,Open Road,Cliffs,WorkShop
x1m2_path,Open Road,Path,WorkShop
x1m3_city,Open Road,City,WorkShop
x1m4_forest,Open Road,Forest,WorkShop
x1m5_salvation,Open Road,Salvation,WorkShop
PR1_Waterfront_F,Parish OverGrowth,Waterfront,WorkShop
PR2_Park_F,Parish OverGrowth,park,WorkShop
PR3_Highway_F,Parish OverGrowth,Highway,WorkShop
PR4_Quarter_F,Parish OverGrowth,Quarter,WorkShop
PR5_Bridge_F,Parish OverGrowth,bridge,WorkShop
l4d2_stadium1_apartment,Suicide Blitz 2,The Apartment Versus,WorkShop
l4d2_vs_stadium2_riverwalk,Suicide Blitz 2,The Riverwalk Versus,WorkShop
l4d2_stadium3_city1,Suicide Blitz 2,The Law Versus,WorkShop
l4d2_stadium4_city2,Suicide Blitz 2,The City Versus,WorkShop
l4d2_stadium5_stadium,Suicide Blitz 2,The Stadium Versus,WorkShop
uz_crash,Undead Zone,Crash,WorkShop
uz_town,Undead Zone,Town,WorkShop
uz_desert,Undead Zone,Desert,WorkShop
uz_bunker,Undead Zone,Bunker,WorkShop
uz_escape,Undead Zone,Escape,WorkShop
uf1_boulevard,Urban Flight,1: Boulevard (VS),WorkShop
uf2_rooftops,Urban Flight,2: Rooftops (VS),WorkShop
uf3_harbor,Urban Flight,3: Harbor (VS),WorkShop
uf4_airfield,Urban Flight,4: Airfield (VS),WorkShop
srocchurch,Warcelona,neighborhood,WorkShop
plaza_espana,Warcelona,plaza,WorkShop
maria_cristina,Warcelona,avenue,WorkShop
mnac,Warcelona,gardens,WorkShop
l4d_tbm_1,Bloody Moors,1: The Cottage,WorkShop
l4d_tbm_2,Bloody Moors,2: Acid House Party,WorkShop
l4d_tbm_3,Bloody Moors,3: 'Keep Off The Moors',WorkShop
l4d_tbm_4,Bloody Moors,4: The Old Stag,WorkShop
l4d_tbm_5,Bloody Moors,5: Arthur's Supplies,WorkShop
cwm1_intro,Carried Off,The Riverbed,WorkShop
cwm2_warehouse,Carried Off,The Town,WorkShop
cwm3_drain,Carried Off,The Sewers,WorkShop
cwm4_building,Carried Off,The Office Building,WorkShop
c2m1_undarkv2,Unforgivable Night Redux,Port,WorkShop
c2m2_undarkv2,Unforgivable Night Redux,Factory,WorkShop
c2m3_undarkv2,Unforgivable Night Redux,Urban,WorkShop
c2m4_undarkv2,Unforgivable Night Redux,Rooftop Construction,WorkShop
dcr_m1_hotel,Dead Center: Rebirth,1: Hotel,WorkShop
dcr_m2_streets,Dead Center: Rebirth,2: Streets,WorkShop
dcr_m3_mall,Dead Center: Rebirth,3: Mall,WorkShop
dcr_m4_atrium,Dead Center: Rebirth,4: Atrium,WorkShop
DCR1_meetup_F,Dead Center: ReConstructed,meetup,WorkShop
DCR2_TheVannha_F,Dead Center: ReConstructed,Vannha,WorkShop
DCR3_Streets_F,Dead Center: ReConstructed,Streets,WorkShop
DCR4_Mallentrance_F,Dead Center: ReConstructed,Mallentrance,WorkShop
DCR5_Mall_F,Dead Center: ReConstructed,Mall,WorkShop
l4d_deathaboard01_prison,Death Aboard II,Prison,WorkShop
l4d_deathaboard02_yard,Death Aboard II,Prison Yard,WorkShop
l4d_deathaboard03_docks,Death Aboard II,Docks,WorkShop
l4d_deathaboard04_ship,Death Aboard II,Ship,WorkShop
l4d_deathaboard05_light,Death Aboard II,Lighthouse,WorkShop
dsr_m1,Death Sentence Redux,Satans Square,WorkShop
dsr_m2,Death Sentence Redux,The Stink of Flesh,WorkShop
dsr_m3,Death Sentence Redux,Hostil Campsite,WorkShop
dsr_m4_sv,Death Sentence Redux,Village of the Damned,WorkShop
dsr_m5,Death Sentence Redux,Slaughter Island,WorkShop
fos1m1_hill,FOS1,fos1m1(VS),WorkShop
fos1m2_fftown,FOS1,fos1m2(VS),WorkShop
fos1m3_factory,FOS1,fos1m3(VS),WorkShop
fos1m4_moors,FOS1,fos1m4(VS),WorkShop
fos1m5_92farm,FOS1,fos1m5(VS),WorkShop
noecho_m1,No Echo Match,noecho_m1 (VS),WorkShop
noecho_m2,No Echo Match,noecho_m2 (VS),WorkShop
noecho_m3,No Echo Match,noecho_m3 (VS),WorkShop
noecho_m4,No Echo Match,noecho_m4 (VS),WorkShop
noecho_m5,No Echo Match,noecho_m5 (VS),WorkShop
outline_m1,Outline,Rise up,WorkShop
outline_m2,Outline,Visit the city,WorkShop
outline_m3,Outline,Through the town,WorkShop
outline_m4,Outline,Rest in yard,WorkShop
tripday_new_m1,Trip day Match,tripday:match (1/5),WorkShop
tripday_new_m2,Trip day Match,tripday:match (2/5),WorkShop
tripday_new_m3,Trip day Match,tripday:match (3/5),WorkShop
tripday_new_m4,Trip day Match,tripday:match (4/5),WorkShop
tripday_new_m5,Trip day Match,tripday:match (5/5),WorkShop
"""

# ========= Config por argumentos ========= #
debug = False
onlyOficial = False
onlyWorkShop = False
cantidad_campañas = 50

# ========= Funciones ========== #
def generar_maplist_csv(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(maplist_default)
    print(f"🆕 Archivo generado: {filename} desde datos embebidos")

def limpiar_capitulos(data, onlyOficial=False, onlyWorkShop=False):
    campañas = {}
    for row in data:
        origen = row.get('Origen', '').strip()
        campaña = row.get('Campaña', '').strip()
        if onlyOficial and origen != 'Oficial':
            continue
        if onlyWorkShop and origen != 'WorkShop':
            continue
        campañas.setdefault(campaña, []).append(row)

    cleaned_data = []
    for campaña, capitulos in campañas.items():
        primeros_4 = capitulos[:4]
        if debug:
            print(f"🧼 {campaña} → {len(primeros_4)} capítulos incluidos")
        cleaned_data.extend(primeros_4)
    return cleaned_data

def agrupar_mapas(data):
    agrupados = {}
    for row in data:
        try:
            campania = row['Campaña'].replace(" ", "")
            capitulo_raw = row['Capitulo'].strip()
            if ':' in capitulo_raw:
                capitulo = int(capitulo_raw.split(':')[0].strip())
            else:
                campaña_grupo = agrupados.get(campania + "_Early", []) + agrupados.get(campania + "_Late", [])
                capitulo = len(campaña_grupo) + 1
            sufijo = "Early" if capitulo <= 2 else "Late"
            grupo = f"{campania}_{sufijo}"
            agrupados.setdefault(grupo, []).append(row['Codigo'])
            if debug: print(f"📦 Agrupado {row['Codigo']} en {grupo}")
        except Exception as e:
            if debug: print(f"❌ Error agrupando fila {row}: {e}")
    return agrupados

def generar_grupos(csv_file, json_output):
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    except Exception as e:
        print(f"❌ Error leyendo CSV '{csv_file}': {e}")
        return None

    if debug: print(f"📄 Total filas en CSV: {len(data)}")
    data_limpia = limpiar_capitulos(data, onlyOficial=onlyOficial, onlyWorkShop=onlyWorkShop)
    mapas_agrupados = agrupar_mapas(data_limpia)

    with open(json_output, "w", encoding='utf-8') as f:
        json.dump(mapas_agrupados, f, indent=4, ensure_ascii=False)
    print(f"✅ Archivo de grupos generado: {json_output}")
    return mapas_agrupados

def crear_combinaciones(agrupados, limite):
    early = [k for k in agrupados if k.endswith("_Early")]
    late = [k for k in agrupados if k.endswith("_Late")]
    combinaciones = set()  # evitar duplicados por nombre

    if debug:
        print(f"🟦 Grupos Early: {early}")
        print(f"🟥 Grupos Late: {late}")

    intentos = 0
    max_intentos = limite * 10  # evitar bucles infinitos

    while len(combinaciones) < limite and intentos < max_intentos:
        e = random.choice(early)
        l = random.choice(late)
        intentos += 1

        if e.split('_')[0] == l.split('_')[0]:
            continue  # evitar misma campaña

        nombre = f"{e.split('_')[0]}_{l.split('_')[0]}"
        if nombre in combinaciones:
            continue  # evitar combinaciones duplicadas por nombre

        if debug:
            print(f"🧪 Combinación: {nombre}")
            print(f"   Mapas: {agrupados[e] + agrupados[l]}")

        combinaciones.add(nombre)

        yield {
            "Nombre": nombre,
            "Mapas": agrupados[e] + agrupados[l],
            "CMD": f"sm_add_map_transition {agrupados[e][-1]} {agrupados[l][0]}"
        }

    early = [k for k in agrupados if k.endswith("_Early")]
    late = [k for k in agrupados if k.endswith("_Late")]
    combinaciones = []
    usados_early = set()
    usados_late = set()

    candidatos = [(e, l) for e in early for l in late if e.split('_')[0] != l.split('_')[0]]
    random.shuffle(candidatos)

    for e, l in candidatos:
        if len(combinaciones) >= limite:
            break
        if e in usados_early or l in usados_late:
            continue
        nombre = f"{e.split('_')[0]}_{l.split('_')[0]}"
        combinaciones.append({
            "Nombre": nombre,
            "Mapas": agrupados[e] + agrupados[l],
            "CMD": f"sm_add_map_transition {agrupados[e][-1]} {agrupados[l][0]}"
        })
        if debug:
            print(f"🧪 Combinación: {nombre}")
            print(f"   Mapas: {agrupados[e] + agrupados[l]}")
        usados_early.add(e)
        usados_late.add(l)
    return combinaciones

def generar_campañas(agrupados, output_file, limite):
    combinaciones = list(crear_combinaciones(agrupados, limite))
    if not combinaciones:
        print("❌ No se generaron combinaciones.")
        return

    resultado = {
        "Cantidad de campañas": len(combinaciones)
    }

    for c in combinaciones:
        resultado[c["Nombre"]] = {
            "Mapas": c["Mapas"],
            "CMD": c["CMD"]
        }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"✅ Archivo de campañas generado: {output_file} 📊 ({len(combinaciones)} combinaciones)")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="Activa modo debug", default=argparse.SUPPRESS)
    parser.add_argument('--oficial', action='store_true', help="Usa solo mapas oficiales", default=argparse.SUPPRESS)
    parser.add_argument('--workshop', action='store_true', help="Usa solo mapas de Workshop", default=argparse.SUPPRESS)
    parser.add_argument('--n', '--cantidad', type=int, help="Cantidad de campañas a generar", default=argparse.SUPPRESS)
    parser.add_argument('--forzar', action='store_true', help="Regenera Grupos.json aunque exista", default=argparse.SUPPRESS)
    return parser.parse_args()

def main():
    global debug, onlyOficial, onlyWorkShop, cantidad_campañas

    args = vars(parse_args())  # convierte a diccionario para evaluar si existe la clave

    # Sobrescribir solo si fueron pasados por CLI
    if 'debug' in args: debug = True
    if 'oficial' in args: onlyOficial = True
    if 'workshop' in args: onlyWorkShop = True
    if 'n' in args: cantidad_campañas = args['n']

    if onlyOficial and onlyWorkShop:
        print("⚠️ No puedes usar --oficial y --workshop al mismo tiempo.")
        return

    if debug:
        print(f"⚙️ Configuración activa: debug={debug}, oficial={onlyOficial}, workshop={onlyWorkShop}, cantidad={cantidad_campañas}")

    # Verifica que exista el archivo Maplist.csv
    csv_file = "Maplist.csv"
    if not os.path.exists(csv_file):
        generar_maplist_csv(csv_file)

    # Cargar el CSV para validaciones
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            datos_csv = list(reader)
    except Exception as e:
        print(f"❌ Error leyendo CSV para verificación: {e}")
        return

    if onlyOficial and not any(row.get("Origen", "").strip() == "Oficial" for row in datos_csv):
        print("❌ No se encontraron mapas oficiales en el archivo CSV.")
        return

    if onlyWorkShop and not any(row.get("Origen", "").strip() == "WorkShop" for row in datos_csv):
        print("❌ No se encontraron mapas de Workshop en el archivo CSV.")
        return

    grupos_json = "Grupos.json"
    campañas_json = "Campañas.json"

    if os.path.exists(grupos_json) and 'forzar' not in args:
        print(f"📂 Usando archivo existente: {grupos_json}")
        with open(grupos_json, "r", encoding="utf-8") as f:
            agrupados = json.load(f)
    else:
        print("♻️ Generando Grupos.json desde CSV...")
        agrupados = generar_grupos(csv_file, grupos_json)
        if agrupados is None:
            return

    generar_campañas(agrupados, campañas_json, cantidad_campañas)

if __name__ == "__main__":
    main()