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
"""

# ========= Config por argumentos ========= #
debug = False
onlyOficial = False
onlyWorkShop = False
cantidad_campañas = 10

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
    combinaciones = crear_combinaciones(agrupados, limite)
    if not combinaciones:
        print("❌ No se generaron combinaciones.")
        return
    resultado = {"Cantidad de campañas": len(combinaciones)}
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
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--oficial', action='store_true')
    parser.add_argument('--workshop', action='store_true')
    parser.add_argument('--n', '--cantidad', type=int, default=10)
    parser.add_argument('--forzar', action='store_true')
    return parser.parse_args()

def main():
    global debug, onlyOficial, onlyWorkShop, cantidad_campañas

    args = parse_args()
    debug = args.debug
    onlyOficial = args.oficial
    onlyWorkShop = args.workshop
    cantidad_campañas = args.n

    if onlyOficial and onlyWorkShop:
        print("⚠️ No puedes usar --oficial y --workshop al mismo tiempo.")
        return

    csv_file = "Maplist.csv"
    if not os.path.exists(csv_file):
        generar_maplist_csv(csv_file)

    grupos_json = "Grupos.json"
    campañas_json = "Campañas.json"

    if os.path.exists(grupos_json) and not args.forzar:
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
