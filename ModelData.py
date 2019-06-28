# Shah, Chirag H.
# 2019-04-30

#---------#---------#---------#---------#---------#--------#
import sys
import math

#----------------------------------------------------------------------
class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.m_Patches  = [] 

    self.m_minX     = float( '+inf' )
    self.m_maxX     = float( '-inf' )
    self.m_minY     = float( '+inf' )
    self.m_maxY     = float( '-inf' )
    self.m_minZ     = float( '+inf' )
    self.m_maxZ     = float( '-inf' )

    self.m_sx       = 1.0
    self.m_ax       = 0.0
    self.m_sy       = 1.0
    self.m_ay       = 0.0
    self.m_distance = 0.0  #I am initializing min. distance as 10.0

    self.m_r00 = 0.0
    self.m_r01 = 0.0
    self.m_r02 = 0.0
    self.m_r10 = 0.0
    self.m_r11 = 0.0
    self.m_r12 = 0.0
    self.m_r02 = 0.0
    self.m_r12 = 0.0
    self.m_r22 = 0.0
    self.m_ex = 0.0
    self.m_ey = 0.0
    self.m_ez = 0.0


    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    with open( inputFile, 'r' ) as fp :
      lines = fp.read().replace('\r', '' ).split( '\n' )

    for ( index, line ) in enumerate( lines, start = 1 ) :
      line = line.strip()
      if ( line == '' or line[ 0 ] == '#' ) :
        continue

      if ( line[ 0 ] == 'v' ) :
        try :
          ( _, x, y, z ) = line.split()
          x = float( x )
          y = float( y )
          z = float( z )

          self.m_minX = min( self.m_minX, x )
          self.m_maxX = max( self.m_maxX, x )
          self.m_minY = min( self.m_minY, y )
          self.m_maxY = max( self.m_maxY, y )
          self.m_minZ = min( self.m_minZ, z )
          self.m_maxZ = max( self.m_maxZ, z )

          self.m_Vertices.append( ( x, y, z ) )

        except :
          print( 'Line %d is a malformed vertex spec.' % index )

      elif ( line[ 0 ] == 'f' ) :
        try :
          ( _, v1, v2, v3 ) = line.split()
          v1 = int( v1 )-1
          v2 = int( v2 )-1
          v3 = int( v3 )-1
          self.m_Faces.append( ( v1, v2, v3 ) )

        except :
          print( 'Line %d is a malformed face spec.' % index )

      elif ( line[ 0 ] == 'w' ) :
        if ( not self.m_Window == [] ) :
          print( 'Line %d is a duplicate window spec.' % index )

        try :
          ( _, xmin, ymin, xmax, ymax ) = line.split()
          xmin = float( xmin )
          ymin = float( ymin )
          xmax = float( xmax )
          ymax = float( ymax )
          self.m_Window = ( xmin, ymin, xmax, ymax )

        except :
          print( 'Line %d is a malformed window spec.' % index )

      elif ( line[ 0 ] == 's' ) :
        if ( not self.m_Viewport == [] ) :
          print( 'Line %d is a duplicate viewport spec.' % index )

        try :
          ( _, xmin, ymin, xmax, ymax ) = line.split()
          xmin = float( xmin )
          ymin = float( ymin )
          xmax = float( xmax )
          ymax = float( ymax )
          self.m_Viewport = ( xmin, ymin, xmax, ymax )

        except :
          print( 'Line %d is a malformed viewport spec.' % index )

      elif ( line[0] == 'p') :
        try :
          ( _, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16 ) = line.split()
          p1 = int( p1 )-1
          p2 = int( p2 )-1
          p3 = int( p3 )-1
          p4 = int( p4 )-1
          p5 = int( p5 )-1
          p6 = int( p6 )-1
          p7 = int( p7 )-1
          p8 = int( p8 )-1
          p9 = int( p9 )-1
          p10 = int( p10 )-1
          p11 = int( p11 )-1
          p12 = int( p12 )-1
          p13 = int( p13 )-1
          p14 = int( p14 )-1
          p15 = int( p15)-1
          p16 = int( p16 )-1
          self.m_Patches.append( ( p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16 ) )

        except :
          print( 'Line %d is a malformed patches spec.' % index )

      else :
          print( 'Line %d \'%s\' is unrecognized.' % ( index, line ) )

  def getBoundingBox( self ) :
    return (
      self.m_minX, self.m_maxX,
      self.m_minY, self.m_maxY,
      self.m_minZ, self.m_maxZ )

  def specifyTransform( self, ax, ay, sx, sy, distance ) :
    self.m_ax = ax
    self.m_sx = sx
    self.m_ay = ay
    self.m_sy = sy
    self.m_distance = distance

  def specifyEuler(self, roll, pitch, yaw): #'φ', 'θ', and 'ψ'
    self.m_r00 = math.cos(yaw) * math.cos(pitch)
    self.m_r10 = (math.cos(roll) * math.sin(yaw)) + (math.cos(yaw)* math.sin(roll) *math.sin(pitch))
    self.m_r20 = - (math.cos(roll) * math.cos(yaw) * math.sin(pitch)) + (math.sin(roll) * math.sin(yaw))
    self.m_r01 = - (math.cos(pitch) * math.sin(yaw))
    self.m_r11 = (math.cos(roll) * math.cos(yaw)) - (math.sin(roll) * math.sin(yaw) * math.sin(pitch))
    self.m_r21 = (math.cos(roll) * math.sin(yaw) * math.sin(pitch)) + (math.cos(yaw) * math.sin(roll))
    self.m_r02 = math.sin(pitch)
    self.m_r12 = - (math.cos(pitch) * math.sin(roll))
    self.m_r22 = math.cos(roll) * math.cos(pitch)
    tx, ty, tz =self.getCenter()#getting the centers
    self.m_ex = - self.m_r00*tx -  self.m_r01*ty - self.m_r02*tz + tx 
    self.m_ey = - self.m_r10*tx -  self.m_r11*ty - self.m_r12*tz + ty
    self.m_ez = - self.m_r20*tx -  self.m_r21*ty - self.m_r22*tz + tz


  def getTransformedVertex( self, vNum, doPerspective, doEuler ) :
    ( x, y, z ) = self.m_Vertices[ vNum ]
    if doEuler:
      rx = self.m_r00*x + self.m_r01*y + self.m_r02*z + self.m_ex  
      ry = self.m_r10*x + self.m_r11*y + self.m_r12*z + self.m_ey
      rz = self.m_r20*x + self.m_r21*y + self.m_r22*z + self.m_ez
      (x, y, z) = (rx, ry, rz)

    if doPerspective :
      #print('Got Perspective : ',doPerspective, x, y, z)
      if self.m_distance > z:
        xx = x / (1-z/self.m_distance)
        yy = y / (1-z/self.m_distance)
      else:
        xx = x
        yy = y
      return ( self.m_sx*xx + self.m_ax, self.m_sy*yy + self.m_ay, 0.0 )
    else :
      #print("Else from ModelData:getTransformedVertex")
      return ( self.m_sx*x + self.m_ax, self.m_sy*y + self.m_ay, 0.0 ) 

  def getCenter( self ) :
    return (
      ( self.m_minX + self.m_maxX ) / 2.0,
      ( self.m_minY + self.m_maxY ) / 2.0,
      ( self.m_minZ + self.m_maxZ ) / 2.0 )

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window
  def getPatches( self )    : return self.m_Patches

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load.
  fName = sys.argv[1]

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( f'{fName}: {len( model.getVertices() )} vert%s, {len( model.getFaces() )} face%s' % (
    'ex' if len( model.getVertices() ) == 1 else 'ices',
    '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( f'     {v}' )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( f'     {f}' )

  print( f'Window line    : {model.getWindow()}' )
  print( f'Viewport line  : {model.getViewport()}' )

  print( f'Center         : {model.getCenter()}' )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
