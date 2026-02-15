# DEFAULT CONSTANTS
DEFAULT_NO_ALLIANCE = {'id':'0', 'name':''}

DEFAULT_NATION_FILTER = {
    'excludeApplicants':False,
    'excludeBeige':False,
    'includeIfBeigeLessThan':2,         # Applies if excludeBeige is True
    'excludeVacation':False,
    'includeIfVacationLessThan':2,      # Applies if excludeVacation is True
    'excludeNoDefSlot':False,
    'excludeNoOffSlot':False
}


# Politics and war defaults
DEFAULT_WAR_TYPES = [
    'RAID',
    'ORDINARY',
    'ATTRITION'
]

DEFAULT_WAR_POLICIES = [
    'ATTRITION',
    'TURTLE',
    'BLITZKRIEG',
    'FORTRESS',
    'MONEYBAGS',
    'PIRATE',
    'TACTICIAN',
    'GUARDIAN',
    'COVERT',
    'ARCANE'
] 

DEFAULT_DOMESTIC_POLICIES = [
    'MANIFEST_DESTINY',
    'OPEN_MARKETS',
    'TECHNOLOGICAL_ADVANCEMENT',
    'IMPERIALISM',
    'URBANIZATION',
    'RAPID_EXPANSION'
]

DEFAULT_COLORS = [
    'aqua',
    'black',
    'blue',
    'brown',
    'green',
    'lime',
    'maroon',
    'olive',
    'orange',
    'pink',
    'purple',
    'red',
    'white',
    'yellow',
    'gold',
    'gray',
    'beige'
]

# DICTs for counting
DEFAULT_WAR_TYPES_DICT = {name: 0 for name in DEFAULT_WAR_TYPES}
DEFAULT_WAR_POLICIES_DICT = {name: 0 for name in DEFAULT_WAR_POLICIES}
DEFAULT_DOMESTIC_POLICIES_DICT = {name: 0 for name in DEFAULT_DOMESTIC_POLICIES}
DEFAULT_COLORS_DICT = {name: 0 for name in DEFAULT_COLORS}


# Helper Classes
class Sphere():
    ALLIANCE = 'alliance'
    SPHERE = 'sphere'
    ENEMY = 'enemy'
    UNALLIED = 'unallied'
    FALLBACK = 'fallback'

    yourAlliance = "4221"
    sphereList = ["3339", "12480", "11009", "7484", "13295"]

    @staticmethod
    def map_allianceID_to_sphere(ID: str):
        if ID == '0':
            return Sphere.UNALLIED
        if ID == Sphere.yourAlliance:
            return Sphere.ALLIANCE
        if ID in Sphere.sphereList:
            return Sphere.SPHERE
        return Sphere.ENEMY

    @staticmethod
    def map_alliance_to_sphere(alliance: dict):
        if alliance == None:
            return Sphere.UNALLIED
        return Sphere.map_allianceID_to_sphere(alliance['id'])

    @staticmethod
    def get(alliance):
        if type(alliance) == str:
            return Sphere.map_allianceID_to_sphere(alliance)
        if type(alliance) == dict:
            return Sphere.map_alliance_to_sphere(alliance)

class Viewport:
    panY = 300

    nodePosLeft = 350

    nodePosRight = 1350
    nodeSpace = 80

    nodeHeight = 60
    nodeWidth = 350

    warNodePos = int((nodePosLeft + nodePosRight) / 2)
    warNodeSpace = 60

    warNodeHeight = 40
    warNodeWidth = 250
