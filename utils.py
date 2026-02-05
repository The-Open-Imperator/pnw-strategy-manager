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
