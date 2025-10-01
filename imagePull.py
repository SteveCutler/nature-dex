import requests
import os
import urllib.request

# Make a folder for images
os.makedirs("inat_dataset", exist_ok=True)

# List of species you want (scientific names work best)
species_list = [
    # Annuals & Biennials
    "Artemisia campestris",
    "Cirsium discolor",
    "Echinocystis lobata",
    "Nicotiana rustica",
    "Oenothera biennis",
    "Phaseolus coccineus",

    # Perennials
    "Achillea millefolium",
    "Acorus americanus",
    "Actaea pachypoda",
    "Actaea racemosa",
    "Actaea rubra",
    "Agastache foeniculum",
    "Agastache scrophulariifolia",
    "Ageratina altissima",
    "Allium cernuum",
    "Allium tricoccum",
    "Amsonia ciliata",
    "Anaphalis margaritacea",
    "Anemone acutiloba",
    "Anemone canadensis",
    "Anemone cylindrica",
    "Antennaria neglecta",
    "Aquilegia canadensis",
    "Aralia racemosa",
    "Argentina anserina",
    "Arisaema triphyllum",
    "Artemisia ludoviciana",
    "Asclepias incarnata",
    "Asclepias tuberosa",
    "Asclepias syriaca",
    "Baptisia australis",
    "Callirhoe digitata",
    "Callirhoe involucrata",
    "Caulophyllum thalictroides",
    "Chelone glabra",
    "Chelone obliqua",
    "Conoclinium coelestinum",
    "Coreopsis grandiflora",
    "Coreopsis lanceolata",
    "Coreopsis tripteris",
    "Dicentra cucullaria",
    "Dodecatheon meadia",
    "Doellingeria umbellata",
    "Echinacea pallida",
    "Echinacea purpurea",
    "Epilobium angustifolium",
    "Erigeron philadelphicus",
    "Erigeron pulchellus",
    "Eryngium yuccifolium",
    "Erythronium americanum",
    "Eupatorium perfoliatum",
    "Eurybia divaricata",
    "Eurybia macrophylla",
    "Euthamia graminifolia",
    "Eutrochium maculatum",
    "Eutrochium purpureum",
    "Filipendula rubra",
    "Fragaria virginiana",
    "Gaultheria procumbens",
    "Geranium maculatum",
    "Geum rivale",
    "Geum triflorum",
    "Gillenia trifoliata",
    "Helenium autumnale",
    "Helenium flexuosum",
    "Helianthus divaricatus",
    "Helianthus giganteus",
    "Heliopsis helianthoides",
    "Heuchera richardsonii",
    "Hydrophyllum virginianum",
    "Hypericum ascyron",
    "Iris versicolor",
    "Liatris ligulistylis",
    "Liatris spicata",
    "Lobelia cardinalis",
    "Lobelia siphilitica",
    "Lupinus perennis",
    "Maianthemum stellatum",
    "Mentha arvensis",
    "Mertensia virginica",
    "Mimulus ringens",
    "Monarda didyma",
    "Monarda fistulosa",
    "Monarda punctata",
    "Oenothera fruticosa",
    "Opuntia humifusa",
    "Packera aurea",
    "Packera paupercula",
    "Parthenium integrifolium",
    "Penstemon digitalis",
    "Penstemon hirsutus",
    "Polygonatum biflorum",
    "Phlox divaricata",
    "Physostegia virginiana",
    "Phytolacca americana",
    "Polemonium reptans",
    "Pycnanthemum virginianum",
    "Ratibida pinnata",
    "Rudbeckia hirta",
    "Rudbeckia laciniata",
    "Rudbeckia triloba",
    "Ruellia humilis",
    "Sanguinaria canadensis",
    "Sanguisorba officinalis",
    "Scrophularia marilandica",
    "Silene stellata",
    "Silphium perfoliatum",
    "Sisyrinchium montanum",
    "Solidago canadensis",
    "Solidago caesia",
    "Solidago flexicaulis",
    "Solidago nemoralis",
    "Solidago ptarmicoides",
    "Solidago rigida",
    "Solidago rugosa",
    "Stylophorum diphyllum",
    "Symphyotrichum laeve",
    "Symphyotrichum novae-angliae",
    "Symphyotrichum oblongifolium",
    "Symphyotrichum oolentangiense",
    "Symphyotrichum puniceum",
    "Symphyotrichum urophyllum",
    "Thalictrum dasycarpum",
    "Tiarella cordifolia",
    "Tradescantia ohiensis",
    "Trillium grandiflorum",
    "Verbena hastata",
    "Verbena stricta",
    "Vernonia gigantea",
    "Vernonia fasciculata",
    "Veronicastrum virginicum",
    "Zizia aurea",

    # Grasses & Sedges
    "Andropogon gerardii",
    "Carex hystericina",
    "Carex muskingumensis",
    "Chasmanthium latifolium",
    "Elymus hystrix",
    "Elymus canadensis",
    "Hierochloe odorata",
    "Panicum acuminatum",
    "Panicum virgatum",
    "Schizachyrium scoparium",
    "Sisyrinchium montanum",
    "Sorghastrum nutans",
    "Spartina pectinata",

    # Pond Plants
    "Acorus americanus",
    "Caltha palustris",
    "Eleocharis palustris",
    "Iris versicolor",
    "Nymphaea odorata",
    "Parnassia glauca",
    "Pontederia cordata",
    "Sagittaria latifolia",
    "Saururus cernuus",

    # Ferns
    "Athyrium filix-femina",
    "Cystopteris bulbifera",
    "Dryopteris intermedia",
    "Dryopteris marginalis",
    "Matteuccia struthiopteris",
    "Osmunda regalis",
    "Polystichum acrostichoides",
    "Onoclea sensibilis",

    # Groundcovers
    "Anaphalis margaritacea",
    "Anemone canadensis",
    "Antennaria neglecta",
    "Apios americana",
    "Argentina anserina",
    "Asarum canadense",
    "Cornus canadensis",
    "Diervilla lonicera",
    "Fragaria virginiana",
    "Hydrophyllum virginianum",
    "Mitchella repens",
    "Podophyllum peltatum",
    "Rubus fragellaris",
    "Tiarella cordifolia",

    # Vines
    "Apios americana",
    "Clematis virginiana",
    "Lonicera sempervirens",
    "Parthenocissus quinquefolia",
    "Rubus fragellaris",

    # Shrubs
    "Amelanchier laevis",
    "Aronia melanocarpa",
    "Ceanothus americanus",
    "Cephalanthus occidentalis",
    "Cornus alternifolia",
    "Cornus amomum",
    "Cornus racemosa",
    "Cornus sericea",
    "Corylus americana",
    "Elaeagnus commutata",
    "Gaultheria procumbens",
    "Hamamelis virginiana",
    "Hypericum prolificum",
    "Lindera benzoin",
    "Lonicera canadensis",
    "Prunus virginiana",
    "Rhus aromatica",
    "Rhus typhina",
    "Rosa palustris",
    "Rosa virginiana",
    "Rubus fragellaris",
    "Rubus occidentalis",
    "Rubus odoratus",
    "Salix bebbiana",
    "Salix discolor",
    "Sambucus canadensis",
    "Sambucus pubens",
    "Spiraea alba",
    "Spiraea tomentosa",
    "Staphylea trifolia",
    "Symphoricarpos albus",
    "Viburnum cassinoides",
    "Viburnum dentatum",
    "Viburnum lentago",

    # Small Trees
    "Cornus alternifolia",
    "Maclura pomifera",
    "Ptelea trifoliata",
    "Staphylea trifolia",

    # Shade Trees
    "Acer pensylvanicum",
    "Acer rubrum",
    "Acer saccharinum",
    "Aesculus glabra",
    "Catalpa speciosa",
    "Carya ovata",
    "Celtis occidentalis",
    "Gleditsia triacanthos",
    "Gymnocladus dioicus",
    "Juglans nigra",
    "Quercus rubra",

    # Conifers
    "Abies balsamea",
    "Picea glauca",
    "Pinus strobus",
    "Thuja occidentalis",
    "Tsuga canadensis",
]


# How many images per species to download
N_IMAGES = 100  

def download_species_images(species_name, n_images=100):
    safe_name = species_name.replace(" ", "_")
    save_dir = os.path.join("/Volumes/Blue Drive/iNatDataset", safe_name)
    os.makedirs(save_dir, exist_ok=True)

    page = 1
    count = 0

    while count < n_images:
        url = f"https://api.inaturalist.org/v1/observations?taxon_name={species_name}&quality_grade=research&photos=true&per_page=30&page={page}"
        r = requests.get(url).json()

        results = r.get("results", [])
        if not results:
            print(f"No more results for {species_name}")
            break

        for obs in results:
            if count >= n_images:
                break

            photos = obs.get("photos", [])
            if not photos:
                continue

            photo_url = photos[0].get("url").replace("square", "medium")  # medium = ~500px
            filename = os.path.join(save_dir, f"{safe_name}_{count}.jpg")

            try:
                urllib.request.urlretrieve(photo_url, filename)
                count += 1
            except Exception as e:
                print(f"Error downloading {photo_url}: {e}")

        page += 1

    print(f"Downloaded {count} images for {species_name}")

# Run for your species list
for sp in species_list:
    download_species_images(sp, N_IMAGES)
