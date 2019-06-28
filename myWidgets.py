# Shah, Chirag H.
# 2019-04-30
import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog

#----------------------------------------------------------------------
from ModelData           import ModelData
from constructTransform  import constructTransform

#----------------------------------------------------------------------
class cl_widgets :
  def __init__( self, ob_root_window, ob_world = [] ) :
    self.ob_root_window = ob_root_window
    self.ob_world = ob_world

    self.m_ModelData = None
    self.isClipped = tk.BooleanVar()
    self.isClipped.set( False )
    self.isPerspective = tk.BooleanVar()
    self.isPerspective.set( False )
    self.m_distance = 1.0

    self.isEuler = tk.BooleanVar()
    self.isEuler.set( False )
    self.m_roll = 0.0
    self.m_pitch = 0.0
    self.m_yaw = 0.0 

    self.m_resolution = 4 #Least value setting it to 4.

    self.menu = cl_menu( self )

    self.toolbar = cl_toolbar( self )

    self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
    self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.statusBar_frame.set( 'This is the status bar' )

    self.ob_canvas_frame = cl_canvas_frame( self )
    self.ob_world.add_canvas( self.ob_canvas_frame.canvas )

#----------------------------------------------------------------------
class cl_canvas_frame :
  def __init__( self, master ) :
    self.master = master
    self.canvas = tk.Canvas(
      master.ob_root_window, width=1, height=1, bg='thistle' )

    self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
    self.canvas.bind( '<Configure>',       self.canvas_resized_callback )
    self.canvas.bind( '<Key>',             self.key_callback )

    self.canvas.bind( '<ButtonPress-1>',   lambda e : self.btn_callback( 'LMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-1>', lambda e : self.btn_callback( 'LMB', 'release', e ) )
    self.canvas.bind( '<B1-Motion>',       lambda e : self.btn_callback( 'LMB', 'motion', e ) )
    self.canvas.bind( '<ButtonPress-2>',   lambda e : self.btn_callback( 'MMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-2>', lambda e : self.btn_callback( 'MMB', 'release', e ) )
    self.canvas.bind( '<B2-Motion>',       lambda e : self.btn_callback( 'MMB', 'motion', e ) )
    self.canvas.bind( '<ButtonPress-3>',   lambda e : self.btn_callback( 'RMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-3>', lambda e : self.btn_callback( 'RMB', 'release', e ) )
    self.canvas.bind( '<B3-Motion>',       lambda e : self.btn_callback( 'RMB', 'motion', e ) )

    self.canvas.bind( '<Up>',              lambda e : self.arrow_callback( 'Up', False, e ) )
    self.canvas.bind( '<Down>',            lambda e : self.arrow_callback( 'Down', False, e ) )
    self.canvas.bind( '<Right>',           lambda e : self.arrow_callback( 'Right', False, e ) )
    self.canvas.bind( '<Left>',            lambda e : self.arrow_callback( 'Left', False, e ) )
    self.canvas.bind( '<Shift-Up>',        lambda e : self.arrow_callback( 'Up', True, e ) )
    self.canvas.bind( '<Shift-Down>',      lambda e : self.arrow_callback( 'Down', True, e ) )
    self.canvas.bind( '<Shift-Right>',     lambda e : self.arrow_callback( 'Right', True, e ) )
    self.canvas.bind( '<Shift-Left>',      lambda e : self.arrow_callback( 'Left', True, e ) )

  def arrow_callback( self, arrow, shift, event ) :
    shiftValue = 'Shift-' if shift else ''
    self.master.statusBar_frame.set( f'{shiftValue}{arrow} arrow pressed.' )

  def btn_callback( self, btn, action, event ) :
    if action == 'press' :
      self.master.statusBar_frame.set( f'{btn} pressed. ({event.x}, {event.y})' )
      self.x = event.x
      self.y = event.y
      self.canvas.focus_set()

    elif action == 'release' :
      self.master.statusBar_frame.set( f'{btn} released. ({event.x}, {event.y})' )
      self.x = None
      self.y = None

    elif action == 'motion' :
      self.master.statusBar_frame.set( f'{btn} dragged. ({event.x}, {event.y})' )
      self.x = event.x
      self.y = event.y

    else :
      self.master.statusBar_frame.set( f'Unknown {btn} action {action}.' )

  def key_callback( self, event ) :
    msg = f'{event.char!r} ({ord( event.char )})' \
      if len( event.char ) > 0 else '<non-printing char>'

    self.master.statusBar_frame.set(
      f'{msg} pressed at ({event.x},{event.y})' )

  def canvas_resized_callback( self, event ) :
    self.canvas.config( width = event.width-4, height = event.height-4 )

    self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.master.statusBar_frame.set(
      f'Canvas width, height ({self.canvas.cget( "width" )}, ' +
      f'{self.canvas.cget( "height" )})' )

    self.canvas.pack()

#----------------------------------------------------------------------
class cl_statusBar_frame( tk.Frame ) :
  def __init__( self, master ) :
    tk.Frame.__init__( self, master )
    self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
    self.label.pack( fill = tk.X )

  def set( self, formatStr, *args ) :
    self.label.config( text = 'chs8824: ' + ( formatStr % args ) )
    self.label.update_idletasks()

  def clear( self ) :
    self.label.config( text='' )
    self.label.update_idletasks()

#----------------------------------------------------------------------
class cl_menu :
  def __init__( self, master ) :
    self.master = master
    self.menu = tk.Menu( master.ob_root_window )
    master.ob_root_window.config( menu = self.menu )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'File', menu = dummy )
    dummy.add_command( label = 'New', command = lambda : self.menu_callback( 'file>new' ) )
    dummy.add_command( label = 'Open...', command = lambda : self.menu_callback( 'file>open' ) )
    dummy.add_separator()
    dummy.add_command( label = 'Exit', command = lambda : self.menu_callback( 'file>exit' ) )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Settings', menu = dummy )
    #dummy.add_command( label = 'Item1', command = lambda : self.menu_callback( 'settings>item1' ) )
    #dummy.add_command( label = 'Item2', command = lambda : self.menu_callback( 'settings>item2' ) )
    dummy.add_checkbutton( label= 'Clip', variable = self.master.isClipped)
    dummy.add_checkbutton( label= 'Perspective', variable = self.master.isPerspective)
    dummy.add_checkbutton( label= 'Euler', variable = self.master.isEuler)

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Help', menu = dummy )
    dummy.add_command( label = 'About...', command = lambda : self.menu_callback( 'help>about' ) )

  def menu_callback( self, which = None ) :
    item = 'menu' if which is None else which
    self.master.statusBar_frame.set( f'{item!r} callback' )

#----------------------------------------------------------------------
class cl_toolbar :
  def __init__( self, master ) :
    self.master = master
    self.toolbar = tk.Frame( master.ob_root_window )
    dummy = tk.Button( self.toolbar, text = 'Resolution', width = 12, command = self.resolution_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )
    
    dummy = tk.Button( self.toolbar, text = 'Distance', width = 16, command = self.distance_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'φ', width = 4, command = lambda *args: self.angle_callback("roll") )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'θ', width = 4, command = lambda *args: self.angle_callback("pitch") )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'ψ', width = 4, command = lambda *args: self.angle_callback("yaw") )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Reset', width = 16, command = self.reset_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Load', width = 16, command = self.load_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Draw', width = 16, command = self.draw_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    self.toolbar.pack( side = tk.TOP, fill = tk.X )

  def distance_callback(self) :
    f = simpledialog.askfloat( "Title", "Prompt?", initialvalue = self.master.m_distance, minvalue = 0.0 )
    if f != None :
      self.master.m_distance = f
      print('Distance now set : ', self.master.m_distance )
      #self.master.statusBar_frame.set( "Distance set to :" , self.master.m_distance )
      self.master.statusBar_frame.set(f'Distance is now {self.master.m_distance}' )
      
    else:
      self.master.statusBar_frame.set( 'Distance set cancelled' )

  def resolution_callback(self) :
    f = simpledialog.askinteger( "Title", "Prompt?", initialvalue = self.master.m_resolution, minvalue = 4 )
    if f != None :
      self.master.m_resolution = f
      print('Resolution now set : ', self.master.m_resolution )
      self.master.statusBar_frame.set(f'Resolution is now {self.master.m_resolution}' )
    else:
      self.master.statusBar_frame.set( 'Resolution set cancelled' )

  def angle_callback(self, angle) :
    #print("Got angle :",angle)
    if angle == "roll":
      f = simpledialog.askfloat( "Title", "Prompt?", initialvalue = self.master.m_roll, minvalue = -360.0 )
      if f != None :
        self.master.m_roll = f
        print('φ : ', self.master.m_roll )
        self.master.statusBar_frame.set(f'φ : {self.master.m_roll}' )
      else:
        self.master.statusBar_frame.set( 'φ set cancelled' )
    elif angle == "pitch":
      f = simpledialog.askfloat( "Title", "Prompt?", initialvalue = self.master.m_pitch, minvalue = -360.0 )
      if f != None :
        self.master.m_pitch = f#Converting angles from degrees to radians.
        print('θ : ', self.master.m_pitch )
        self.master.statusBar_frame.set(f'θ: {self.master.m_pitch}' )
      else:
        self.master.statusBar_frame.set( 'θ set cancelled' )
    elif angle == "yaw":
      f = simpledialog.askfloat( "Title", "Prompt?", initialvalue = self.master.m_yaw, minvalue = -360.0 )
      if f != None :
        self.master.m_yaw = f#Converting angles from degrees to radians.
        print('ψ : ', self.master.m_yaw )
        self.master.statusBar_frame.set(f'ψ: {self.master.m_yaw}' )
      else:
        self.master.statusBar_frame.set( 'ψ set cancelled' )
    else:
      print("No angle received")

  def reset_callback( self ) :
    self.master.ob_world.reset()
    self.master.statusBar_frame.set( 'Reset callback' )

  def load_callback( self ) :
    fName = tk.filedialog.askopenfilename( filetypes = [ ( "allfiles", "*" ) ] )
    if ( len( fName ) == 0 ) :
        self.master.statusBar_frame.set( "%s", "[Load was cancelled]" )

    else :
      self.master.m_ModelData = ModelData( fName )

      print( f'---Load {fName!r}' )
      #print(  'Window line   :', self.master.m_ModelData.getWindow() )
      #print(  'Viewport line :', self.master.m_ModelData.getViewport() )
      #print(  'Bounding box  :', self.master.m_ModelData.getBoundingBox() )

      self.master.statusBar_frame.set( 'Load callback' )

  def draw_callback( self ) :

    #print("Got clipp value: ",self.master.isClipped.get())
    if self.master.m_ModelData is None :
      self.master.statusBar_frame.set( 'No model loaded.' )
      return

    width  = int( self.master.ob_canvas_frame.canvas.cget( "width" ) )
    height = int( self.master.ob_canvas_frame.canvas.cget( "height" ) )

    w = self.master.m_ModelData.getWindow()
    v = self.master.m_ModelData.getViewport()

    ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )

    self.master.m_ModelData.specifyTransform( ax, ay, sx, sy, self.master.m_distance )
    #tx,ty,tz = self.master.m_ModelData.getCenter()
    #Converting angles from degrees to radians.
    self.master.m_ModelData.specifyEuler(math.radians(self.master.m_roll), math.radians(self.master.m_pitch), math.radians(self.master.m_yaw))
    #print(  '---Draw' )
    #print( f'Canvas size   : ({width}, {height})' )
    #print( f'Transform     : ax {ax:.3f} ay {ay:.3f} sx {sx:.3f} sy {sy:.3f}' )

    self.master.ob_world.create_graphic_objects( self.master.ob_canvas_frame.canvas, self.master.m_ModelData, self.master.isClipped.get(), self.master.isPerspective.get(), self.master.isEuler.get(), self.master.m_resolution )

    vxMin = v[0] * width
    vxMax = v[2] * width
    vyMin = v[1] * height
    vyMax = v[3] * height
    self.master.ob_canvas_frame.canvas.create_line(vxMin, vyMin, vxMin, vyMax, vxMax, vyMax, vxMax, vyMin, vxMin, vyMin )

    self.master.statusBar_frame.set( 'Draw callback' )
    degree = '\u00b0'
    self.master.statusBar_frame.set(f'Resolution: {self.master.m_resolution} Distance : {self.master.m_distance}     φ : {self.master.m_roll}{degree}      θ: {self.master.m_pitch}{degree}       ψ: {self.master.m_yaw}{degree} ' )
#----------------------------------------------------------------------
