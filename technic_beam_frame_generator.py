import adsk.core, adsk.fusion
import math
import traceback

def getAllItensInSketchProfile(sketch:adsk.fusion.Sketch)->adsk.core.ObjectCollection:
    saida = adsk.core.ObjectCollection.create()
    for prof in sketch.profiles:
        saida.add(prof)
    return saida

def generateBaseFrame(sketch:adsk.fusion.Sketch,sizeX:float,sizeY:float,beamWidth:float,outerRadius:float):
    uPointA = adsk.core.Point3D.create(0, 0, 0)
    uPointB = adsk.core.Point3D.create(sizeX, sizeY, 0)
    frameOuterRectangle = sketch.sketchCurves.sketchLines.addTwoPointRectangle(uPointA, uPointB)
    pickupNeckFillet1 = sketch.sketchCurves.sketchArcs.addFillet(frameOuterRectangle[0], frameOuterRectangle[0].endSketchPoint.geometry, frameOuterRectangle[1], frameOuterRectangle[1].startSketchPoint.geometry, outerRadius)
    pickupNeckFillet1 = sketch.sketchCurves.sketchArcs.addFillet(frameOuterRectangle[1], frameOuterRectangle[1].endSketchPoint.geometry, frameOuterRectangle[2], frameOuterRectangle[2].startSketchPoint.geometry, outerRadius)
    pickupNeckFillet1 = sketch.sketchCurves.sketchArcs.addFillet(frameOuterRectangle[2], frameOuterRectangle[2].endSketchPoint.geometry, frameOuterRectangle[3], frameOuterRectangle[3].startSketchPoint.geometry, outerRadius)
    pickupNeckFillet1 = sketch.sketchCurves.sketchArcs.addFillet(frameOuterRectangle[3], frameOuterRectangle[3].endSketchPoint.geometry, frameOuterRectangle[0], frameOuterRectangle[0].startSketchPoint.geometry, outerRadius)
    uPointG = adsk.core.Point3D.create(0+beamWidth, 0+beamWidth, 0)
    uPointH = adsk.core.Point3D.create(sizeX-beamWidth, sizeY-beamWidth, 0)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(uPointG, uPointH)

def generateBaseMount(sketch:adsk.fusion.Sketch,sizeX:float,sizeY:float,beamWidth:float):
    uPointG = adsk.core.Point3D.create(0+beamWidth, 0+beamWidth, 0)
    uPointH = adsk.core.Point3D.create(sizeX-beamWidth, sizeY-beamWidth, 0)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(uPointG, uPointH)


def generateHolesPlaneXY(sketch:adsk.fusion.Sketch,sizeX:float,sizeY:float,radius:float,beamWidth:float,interHolesDist:float,holesX:int,holesY:int):
    circles = sketch.sketchCurves.sketchCircles
    for i in range(0,holesY,2):
        center = adsk.core.Point3D.create( beamWidth/2,  i * interHolesDist+beamWidth/2, 0)
        circles.addByCenterRadius(center, radius)
        center = adsk.core.Point3D.create( sizeX-beamWidth/2, i * interHolesDist+beamWidth/2, 0)
        circles.addByCenterRadius(center, radius)
    for i in range(2,holesX,2):
        center = adsk.core.Point3D.create(   i * interHolesDist+beamWidth/2,beamWidth/2, 0)
        circles.addByCenterRadius(center, radius)
        center = adsk.core.Point3D.create(  i * interHolesDist+beamWidth/2,sizeY-beamWidth/2, 0)
        circles.addByCenterRadius(center, radius)

def generateHolesPlaneXZ(sketch:adsk.fusion.Sketch,radius:float,beamWidth:float,interHolesDist:float,holesX:int):
    circles = sketch.sketchCurves.sketchCircles
    for i in range(1,holesX,2):
        center = adsk.core.Point3D.create(   i * interHolesDist+beamWidth/2,-beamWidth/2, 0)
        circles.addByCenterRadius(center, radius)

def generateHolesPlaneYZ(sketch:adsk.fusion.Sketch,radius:float,holesY:int,beamWidth:float,interHolesDist:float):
    circles = sketch.sketchCurves.sketchCircles
    for i in range(1,holesY,2):
        center = adsk.core.Point3D.create(- beamWidth/2,  i * interHolesDist+beamWidth/2, 0)
        circles.addByCenterRadius(center, radius)

def generateHolesBoard(sketch:adsk.fusion.Sketch,radius:float,boardMetadata,sizeX:float,sizeY:float):
    diffX = (sizeX - boardMetadata['sizeX'])/2
    diffY = (sizeY - boardMetadata['sizeY'])/2
    circles = sketch.sketchCurves.sketchCircles
    for r in boardMetadata['roles']:
        center = adsk.core.Point3D.create(diffX+r['X'], sizeY- diffY-r['Y'], 0)
        circles.addByCenterRadius(center, radius)

def getBoardMetadata(boardName:str):
    if (boardName=="Arduino Uno"):
        return {'name':'Arduino Uno','sizeX':6.86,'sizeY':5.33,'roles':[{'X':1.4,'Y':0.25,'Diameter':0.32},{'X':1.5,'Y':0.25,'Diameter':0.32},{'X':6.61,'Y':0.76,'Diameter':0.32},{'X':6.61,'Y':3.55,'Diameter':0.32},{'X':1.53,'Y':5.07,'Diameter':0.32}],'AlignmentPoint':None}
    if (boardName=="L298N"):
        return {'name':'L298N','sizeX':4.3,'sizeY':4.3,'roles':[{'X':0.3,'Y':0.3,'Diameter':0.32},{'X':0.3,'Y':4.0,'Diameter':0.32},{'X':4.0,'Y':4.0,'Diameter':0.32},{'X':4.0,'Y':0.3,'Diameter':0.32}],'AlignmentPoint':None}
    if (boardName=="18650 Shield V3"):
        return {'name':'18650 Shield V3','sizeX':2.91,'sizeY':9.94,'roles':[{'X':0.23,'Y':0.23,'Diameter':0.31},{'X':2.7,'Y':0.23,'Diameter':0.31},{'X':2.7,'Y':9.7,'Diameter':0.31},{'X':0.23,'Y':9.7,'Diameter':0.31}],'AlignmentPoint':None}
    if (boardName=="TTGO-T-Cell"):
        return {'name':'TTGO-T-Cell','sizeX':2.83,'sizeY':9.02,'roles':[{'X':0.26,'Y':0.26,'Diameter':0.22},{'X':2.57,'Y':0.26,'Diameter':0.22},{'X':2.57,'Y':8.76,'Diameter':0.22},{'X':0.23,'Y':8.76,'Diameter':0.22}],'AlignmentPoint':None}
    if (boardName=="Raspberry Pi 4"):
        return {'name':'Raspberry Pi 4','sizeX':8.5,'sizeY':5.6,'roles':[{'X':0.35,'Y':0.35,'Diameter':0.27},{'X':6.15,'Y':0.35,'Diameter':0.27},{'X':6.15,'Y':5.25,'Diameter':0.27},{'X':0.35,'Y':5.25,'Diameter':0.27}],'AlignmentPoint':None}
    if (boardName=="Raspberry Pi Zero"):
        return {'name':'Raspberry Pi Zero','sizeX':6.5,'sizeY':3.0,'roles':[{'X':0.35,'Y':0.35,'Diameter':0.275},{'X':6.15,'Y':0.35,'Diameter':0.275},{'X':6.15,'Y':2.65,'Diameter':0.275},{'X':0.35,'Y':2.65,'Diameter':0.275}],'AlignmentPoint':None}
    return None


def exportCompBodyAsSTL(app):
    ui = app.userInterface
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        exportMgr = design.exportManager
        outDir = "D:\Fusion360"

        for comp in design.allComponents:
            for body in comp.bRepBodies:
                fileName = outDir + "/" + body.name

                # create stl exportOptions
                stlExportOptions = exportMgr.createSTLExportOptions(body, fileName)
                stlExportOptions.sendToPrintUtility = False
                
                exportMgr.execute(stlExportOptions)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        ui = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        thickness = 0.15
        beamWidth = 0.78
        interHolesDist =  0.8
        innerRadius = 0.24
        middleRadius = 0.31
        outerRadius = 0.39
        outerRadius = 0.369
        pinStandoff = 0.07
        mountWidth = 0.08

        #board = getBoardMetadata("Raspberry Pi Zero")
        board = getBoardMetadata("Raspberry Pi 4")
        #board = getBoardMetadata("TTGO-T-Cell")
        #board = getBoardMetadata("18650 Shield V3")
        #board = getBoardMetadata("L298N")
        #board = getBoardMetadata("Arduino Uno")


        holesX =math.ceil( (board['sizeX']+beamWidth*2)/0.8 )
        if holesX < 5:
            holesX = 5
        if holesX % 2 == 0:
            holesX = holesX +1
        holesY =math.ceil( (board['sizeY']+beamWidth*2)/0.8 )
        if holesY < 5:
            holesY = 5
        if holesY % 2 == 0:
            holesY = holesY +1
        #Project variables
        #holesX = 7
        #holesY = 11
        sizeX = 0.8*holesX-0.02
        sizeY = 0.8*holesY-0.02        

        #ui.messageBox('Generating Model...'+str(holesX)+' by '+str(holesY)+' roles')

        distance1 = adsk.core.ValueInput.createByReal(beamWidth)
        distance2 = adsk.core.ValueInput.createByReal(sizeY-beamWidth)
        distance3 = adsk.core.ValueInput.createByReal(sizeY)
        distance4 = adsk.core.ValueInput.createByReal(sizeX-beamWidth)
        distance5 = adsk.core.ValueInput.createByReal(sizeX)
        distance6 = adsk.core.ValueInput.createByReal(mountWidth)


        #All the 6 planes needed to create the lego frame
        sketches = rootComp.sketches
        xyPlane1 = rootComp.xYConstructionPlane
        xzPlane1 = rootComp.xZConstructionPlane
        yzPlane1 = rootComp.yZConstructionPlane
        planes = rootComp.constructionPlanes

        planeInput = planes.createInput()
        planeInput.setByOffset(xyPlane1, distance1)
        xyPlane2 = planes.add(planeInput)

        planeInput = planes.createInput()
        planeInput.setByOffset(xzPlane1, distance1)
        xzPlane2 = planes.add(planeInput)
        planeInput = planes.createInput()
        planeInput.setByOffset(xzPlane1, distance2)
        xzPlane3 = planes.add(planeInput)
        planeInput = planes.createInput()
        planeInput.setByOffset(xzPlane1, distance3)
        xzPlane4 = planes.add(planeInput)

        planeInput = planes.createInput()
        planeInput.setByOffset(yzPlane1, distance1)
        yzPlane2 = planes.add(planeInput)
        planeInput = planes.createInput()
        planeInput.setByOffset(yzPlane1, distance4)
        yzPlane3 = planes.add(planeInput)
        planeInput = planes.createInput()
        planeInput.setByOffset(yzPlane1, distance5)
        yzPlane4 = planes.add(planeInput)


        #Base frame
        sketch1 = sketches.add(xyPlane1)
        generateBaseFrame(sketch1,sizeX,sizeY,beamWidth,outerRadius)
        extrudes = rootComp.features.extrudeFeatures
        prof1 = sketch1.profiles.item(0)
        extrude1 = extrudes.addSimple(prof1, distance1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) 

        #Top holes     
        sketch4 = sketches.add(xyPlane1)
        generateHolesPlaneXY(sketch4,sizeX,sizeY,innerRadius,beamWidth,interHolesDist,holesX,holesY)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch4), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setDistanceExtent(False, distance1)
        extrude = extrudes.add(extrudeInput)
        
        #Sketch hole bottom
        sketch5 = sketches.add(xyPlane1)
        generateHolesPlaneXY(sketch5,sizeX,sizeY,middleRadius,beamWidth,interHolesDist,holesX,holesY)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch5), adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance2 = adsk.core.ValueInput.createByReal(pinStandoff)
        extrudeInput.setDistanceExtent(False, distance2)
        extrude = extrudes.add(extrudeInput)

        sketch6 = sketches.add(xyPlane2)
        generateHolesPlaneXY(sketch6,sizeX,sizeY,middleRadius,beamWidth,interHolesDist,holesX,holesY)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch6), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.NegativeExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch7 = sketches.add(xzPlane1)
        generateHolesPlaneXZ(sketch7,innerRadius,beamWidth,interHolesDist,holesX)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch7), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.ThroughAllExtentDefinition.create(), adsk.fusion.ExtentDirections.PositiveExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch8 = sketches.add(xzPlane1)
        generateHolesPlaneXZ(sketch8,middleRadius,beamWidth,interHolesDist,holesX)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch8), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.PositiveExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch9 = sketches.add(xzPlane2)
        generateHolesPlaneXZ(sketch9,middleRadius,beamWidth,interHolesDist,holesX)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch9), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.NegativeExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch10 = sketches.add(xzPlane3)
        generateHolesPlaneXZ(sketch10,middleRadius,beamWidth,interHolesDist,holesX)    
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch10), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.PositiveExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch11 = sketches.add(xzPlane4)
        generateHolesPlaneXZ(sketch11,middleRadius,beamWidth,interHolesDist,holesX)    
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch11), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.NegativeExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch12 = sketches.add( yzPlane1)
        generateHolesPlaneYZ(sketch12,innerRadius,holesY,beamWidth,interHolesDist)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch12), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.ThroughAllExtentDefinition.create(), adsk.fusion.ExtentDirections.PositiveExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch13 = sketches.add( yzPlane1)
        generateHolesPlaneYZ(sketch13,middleRadius,holesY,beamWidth,interHolesDist)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch13), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.PositiveExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch14 = sketches.add( yzPlane2)
        generateHolesPlaneYZ(sketch14,middleRadius,holesY,beamWidth,interHolesDist)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch14), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.NegativeExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch15 = sketches.add( yzPlane3)
        generateHolesPlaneYZ(sketch15,middleRadius,holesY,beamWidth,interHolesDist)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch15), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.PositiveExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        sketch16 = sketches.add( yzPlane4)
        generateHolesPlaneYZ(sketch16,middleRadius,holesY,beamWidth,interHolesDist)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch16), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent( adsk.fusion.DistanceExtentDefinition.create(distance2), adsk.fusion.ExtentDirections.NegativeExtentDirection)  
        extrude = extrudes.add(extrudeInput)

        #generating base mount
        sketch17 = sketches.add( xyPlane1)
        generateBaseMount(sketch17,sizeX,sizeY,beamWidth)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch17), adsk.fusion.FeatureOperations.JoinFeatureOperation)
        extrudeInput.setDistanceExtent(False, distance6)
        extrude = extrudes.add(extrudeInput)

        sketch18 = sketches.add( xyPlane1)
        generateHolesBoard(sketch18,0.35/2,board,sizeX,sizeY)
        extrudeInput = extrudes.createInput(getAllItensInSketchProfile(sketch18), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setDistanceExtent(False, distance6)
        extrude = extrudes.add(extrudeInput)
        

        extrude.bodies.item(0).name = board['name']

        exportCompBodyAsSTL(app)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))