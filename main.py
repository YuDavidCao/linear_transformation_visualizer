from object_3d import *
from camera import *
from projection import *
import pygame as pg
import square
from concurrent import futures
from control import Control
from sys import exit

class SoftwareRender:
    def __init__(self) -> None:
        self.setting = {
            "clipping_mode": False,
            "show_coordinates": False,
            "show_basis_axis": True,
            "show_camera_coordinate": True,
            "animation_duration": 10000,
            "mode": "square",
            "show_vertices": True,
            "inverse": False,
            "transpose": False,
            "grid_size": 3,
            "grid_gap": 1,
            "bg_color": "white",
            "show_animation": True
        } 
        pool.submit(self.tkinit)
        pg.init()
        pg.display.set_caption('display')
        self.HEIGHT = 900
        self.WIDTH  = 1600
        self.RES = self.WIDTH, self.HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.vectors = [
            np.array([1, 1, 1, 1]),
        ]
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()  
   
    def tkinit(self):
        try:
            Control("Control",self)
        except Exception as e:
            print(e)

    def generate_grid(self):
        print(self.setting["grid_gap"])
        grid_size = (self.setting["grid_size"], self.setting["grid_size"], self.setting["grid_size"])
        half_size = np.array(grid_size) // 2
        vertices = np.array([(x * self.setting["grid_gap"], y * self.setting["grid_gap"], z * self.setting["grid_gap"], 1) 
                            for x in range(-half_size[0], half_size[0] + 1) 
                            for y in range(-half_size[1], half_size[1] + 1) 
                            for z in range(-half_size[2], half_size[2] + 1)])
        faces = []
        for x in range(grid_size[0] - 1):
            for y in range(grid_size[1] - 1):
                for z in range(grid_size[2] - 1):
                    v0 = x * grid_size[1] * grid_size[2] + y * grid_size[2] + z
                    v1 = v0 + 1
                    v2 = v0 + grid_size[2]
                    v3 = v2 + 1
                    v4 = v0 + grid_size[1] * grid_size[2]
                    v5 = v4 + 1
                    v6 = v4 + grid_size[2]
                    v7 = v6 + 1
                    faces.extend([(v0, v1, v3, v2), (v4, v5, v7, v6), (v0, v4, v5, v1), (v2, v3, v7, v6), (v1, v5, v7, v3), (v0, v4, v6, v2)])
        faces = np.array(faces)
        self.object = Object3D(
            self,
            vertices=vertices,
            faces=faces,
            animation=self.animation,
            transformation=self.change_coordinate_matrix,
        )

    def change_object(self):
        if(self.setting["mode"] == "grid"):
            self.generate_grid()
        elif(self.setting["mode"] == "square"):
            self.object = Object3D(
                self,
                vertices=square.sqaure_vertices,
                faces=square.square_faces,
                animation=self.animation,
                transformation=self.change_coordinate_matrix,
            )
        elif(self.setting["mode"] == "vector"):
            self.object = Object3D(
                self,
                vertices=self.vectors + [np.array([0, 0, 0, 1])],
                faces=[
                    [i, len(self.vectors)] for i in range(len(self.vectors))
                ],
                animation=self.animation,
                transformation=self.change_coordinate_matrix,
            )

    def create_objects(self):
        self.change_coordinate_matrix = np.array(
            [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
        )
        self.animation = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ], dtype=float
        )
        self.camera = Camera(self, [3,1,-4])
        self.camera.camera_pitch(0.1)
        self.camera.camera_yaw(-math.pi/6)
        self.projection = Projection(self)
        self.change_object()
        self.axis = Axis(self, transformation=self.change_coordinate_matrix, animation=self.animation)
        self.axis.translate([0.5, 0.5, 0.5])
        self.change_axis()


    def change_axis(self):
        self.world_axis = Axis(self, transformation=self.change_coordinate_matrix)
        self.world_axis.movement_flag = False
        self.world_axis.scale(2 * (self.setting["grid_size"] // 2) * self.setting["grid_gap"])
        self.world_axis.translate([0.0001, 0.0001, 0.0001]) 

    def draw_3d_render_area(self):
        pg.draw.polygon(
            self.screen,
            pg.Color("white"),
            [[0, 0], [self.RES[0], 0], self.RES, [0, self.RES[1]]],
            3,
        )

    def draw(self):
        self.screen.fill(pg.Color(self.setting["bg_color"]))
        if(self.setting["show_camera_coordinate"]):
            self.camera.display_coord()
        if(self.setting["show_basis_axis"]):
            self.axis.draw()
        self.object.draw()
        self.world_axis.draw()
        # self.draw_3d_render_area()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    
    pool = futures.ThreadPoolExecutor(max_workers=10)
    np.set_printoptions(suppress=True, formatter={"float": "{:0.02f}".format})
    app = SoftwareRender()
    app.run()
