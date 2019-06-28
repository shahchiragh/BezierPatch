# Shah, Chirag H.
# 2019-04-30

import CohenSutherland as CSL
import numpy 
class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas, modelData, doClip, doPerspective, doEuler, m_resolution) :
    width, height = int(canvas.cget('width')), int(canvas.cget('height'))
    vp = modelData.getViewport() #Get viewport
    viewport = (vp[0] * width, vp[1] * height,  vp[2] * width, vp[3] * height)
    

    if doClip != True:
      for v1Num, v2Num, v3Num in modelData.getFaces() :
        #print("Am I coming here?")
        x1, y1, _ = modelData.getTransformedVertex( v1Num, doPerspective, doEuler )
        x2, y2, _ = modelData.getTransformedVertex( v2Num, doPerspective, doEuler )
        x3, y3, _ = modelData.getTransformedVertex( v3Num, doPerspective, doEuler)
        canvas.create_line( x1, y1, x2, y2, x3, y3, x1, y1 )
    else:
      for v1Num, v2Num, v3Num in modelData.getFaces() :
        x1, y1, _ = modelData.getTransformedVertex( v1Num, doPerspective, doEuler )
        x2, y2, _ = modelData.getTransformedVertex( v2Num, doPerspective, doEuler )
        x3, y3, _ = modelData.getTransformedVertex( v3Num, doPerspective, doEuler )

        for (ax, ay, bx, by) in [(x1,y1,x2,y2), (x2,y2,x3,y3), (x3,y3,x1,y1)]:
          doDraw, p1x, p1y, p2x, p2y = CSL.clipLine(ax,ay,bx,by,viewport) 
          if doDraw:
            canvas.create_line(p1x,p1y,p2x,p2y)
    #print("Coming here..",m_resolution)

    if m_resolution > 0:
      for patch in modelData.getPatches() :
        #print("Patch",patch)
        pointList = []
        controlPoints =[]
        for vNum in patch:
          px, py, pz = modelData.getTransformedVertex( vNum, doPerspective, doEuler )
          controlPoints.append((px, py, pz))
        #print("got control points..",controlPoints)
        pointList = self.resolveBezierPatch(m_resolution,controlPoints)
        #print("Got point list length",pointList)
        for row in range(m_resolution-1):
          rowStart = row * m_resolution
          for col in range(m_resolution-1):
            here = rowStart+col
            there = here + m_resolution
            #print("This Values:",(pointList[here], pointList[there], pointList[there+1]))
            triangleA = (pointList[here], pointList[there], pointList[there+1])
            triangleB = (pointList[there+1], pointList[here+1], pointList[here])
            #print("got trinaglA..", triangleA)
            #print("got trinaglB..")
            self.drawTriangle(canvas, *triangleA, viewport, doClip)
            self.drawTriangle(canvas, *triangleB, viewport, doClip)

  def drawTriangle(self,canvas, v1,v2,v3, portal, doClip) :
    #print("got triangle",triangle)
    #v1, v2 , v3 = triangle
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    x3, y3, z3 = v3
    if doClip:
      for (ax, ay, bx, by) in [(x1,y1,x2,y2), (x2,y2,x3,y3), (x3,y3,x1,y1)]:
        doDraw, p1x, p1y, p2x, p2y = CSL.clipLine(ax,ay,bx,by,portal) 
        if doDraw:
          canvas.create_line(p1x,p1y,p2x,p2y)
    else:
      canvas.create_line( x1, y1, x2, y2, x3, y3, x1, y1 )
    

  def resolveBezierPatch(self, resolution, ctrlPts):
    r_pointList = []
    #print("Got u and v boundry:",numpy.linspace(0.0, 1.0, resolution))
    for u in numpy.linspace(0.0, 1.0, resolution):
      for v in numpy.linspace(0.0, 1.0, resolution):
        point = (0.0, 0.0, 0.0)
        for i in range(4):
          for j in range(4):
            c = self.calculateCoefficients(i,j,u,v)
            #print("Got Coefficient",i,j,u,v," value:",c)
            point = tuple(map(sum, zip(point, self.caluclateEachPoint(c,i,j,ctrlPts))))
            #print("Got Point: ",point)
        r_pointList.append((point))
    #print("Got PointList",pointList)
    return r_pointList

  def caluclateEachPoint(self, c, i, j, ctrlPts):
    points = [[ctrlPts[0],ctrlPts[1],ctrlPts[2],ctrlPts[3]], [ctrlPts[4], ctrlPts[5], ctrlPts[6], ctrlPts[7]], [ctrlPts[8],ctrlPts[9], ctrlPts[10], ctrlPts[11]],[ctrlPts[12],ctrlPts[13],ctrlPts[14],ctrlPts[15]]]
    #print("getting point at",i,j," value:",points[i][j])
    x, y , z = points[i][j]
    getPoints = (c*x, c*y, c*z)
    #print("Got Point: ",getPoints)
    return getPoints

  def calculateCoefficients(self,i,j,u,v):

    c00 = (-u+1)*(-u+1)*(-u+1)*(-v+1)*(-v+1)*(-v+1)
    c01 = 3*v*(-u+1)*(-u+1)*(-u+1)*(-v+1)*(-v+1)
    c02 = 3*v*v*(-u+1)*(-u+1)*(-u+1)*(-v+1)
    c03 = v*v*v*(-u+1)*(-u+1)*(-u+1)

    c10 = 3*u*(-u+1)*(-u+1)*(-v+1)*(-v+1)*(-v+1)
    c11 = 9*u*v*(-u+1)*(-u+1)*(-v+1)*(-v+1)
    c12 = 9*u*v*v*(-u+1)*(-u+1)*(-v+1)
    c13 = 3*u*v*v*v*(-u+1)*(-u+1)

    c20 = 3*u*u*(-u+1)*(-v+1)*(-v+1)*(-v+1)
    c21 = 9*u*u*v*(-u+1)*(-v+1)*(-v+1)
    c22 = 9*u*u*v*v*(-u+1)*(-v+1)
    c23 = 3*u*u*v*v*v*(-u+1)

    c30 = u*u*u*(-v+1)*(-v+1)*(-v+1)
    c31 = 3*u*u*u*v*(-v+1)*(-v+1)
    c32 = 3*u*u*u*v*v*(-v+1)
    c33 = u*u*u*v*v*v
    c = [[c00, c01, c02, c03], [c10, c11, c12, c13], [c20, c21, c22, c23],[c30, c31, c32, c33]]
    computedValue = c[i][j]
    #print("Computed Value",computedValue)
    return computedValue


  def redisplay( self, canvas, event ) :
    pass

#----------------------------------------------------------------------
