import pygame as pg
from matrix_functions import *
from numba import njit
import copy

@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))

class Object3D:
    def __init__(
        self,
        render,
        vertices,
        faces,
        transformation=np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        ),
        animation=np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        ),
        type = "object"
    ) -> None:
        self.render = render
        self.vertices = vertices
        self.faces = faces
        self.font = pg.font.SysFont("Arial", 25, bold=True)
        self.color_faces = [(pg.Color("orange"), face) for face in self.faces]
        self.movement_flag = True
        self.label = ""
        self.animation = animation
        self.transformation = transformation

    def movement(self):
        self.rotate_y(pg.time.get_ticks() % 0.005)

    def get_animation_step(self):
        new = copy.deepcopy(self.animation)
        if(self.render.setting["transpose"]):
            transpose(new)
        if(self.render.setting["inverse"]):
            try:
                inverse(new)
            except:
                pass
        if(not self.render.setting["show_animation"]):
            return new
        diff = new - np.identity(4)
        return (
            np.identity(4)
            + diff
            * (pg.time.get_ticks() % self.render.setting["animation_duration"])
            / self.render.setting["animation_duration"]
        )

    def draw(self):
        # self.movement()
        # if(pg.time.get_ticks() < 10000):
        #     self.vertices = self.vertices @ self.animation
        self.screen_projection()

    def screen_projection(self):
        # print(self.render.animation)
        vertices = self.vertices @ self.get_animation_step()
        coord_v = copy.deepcopy(vertices)
        vertices = vertices @ self.transformation
        vertices = vertices @ self.render.camera.camera_matrix()
        original_v = copy.deepcopy(vertices)
        invalid = [True for _ in range(len(vertices))]
        for row_index in range(len(vertices)):
            if vertices[row_index][2] < 0:
                invalid[row_index] = False
        vertices = vertices @ self.render.projection.projection_matrix
        if self.render.setting["clipping_mode"]:
            vertices[(vertices > 1) | (vertices < -1)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)  # normalization step
        vertices = vertices[:, :2]
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            found = False
            for i in face:
                if not invalid[i]:
                    found = True
                    break
            if found:
                continue
            polygon = vertices[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon, 3)
                if self.label:
                    text = self.font.render(
                        self.label[index], True, pg.Color("white" if self.render.setting["bg_color"] == "black" else "black")
                    )
                    self.render.screen.blit(text, polygon[-1])

        if self.render.setting["show_vertices"]:
            for index, vertex in enumerate(vertices):
                if invalid[index] and not any_func(
                    vertex, self.render.H_WIDTH, self.render.H_HEIGHT
                ):
                    pg.draw.circle(
                        self.render.screen,
                        pg.Color("white" if self.render.setting["bg_color"] == "black" else "black"),
                        vertex,
                        25 / original_v[index][2],
                    )
        
        if self.render.setting["show_coordinates"] and self.render.setting["grid_size"] <= 5:
            for index, vertex in enumerate(vertices):
                if invalid[index] and not any_func(
                    vertex, self.render.H_WIDTH, self.render.H_HEIGHT
                ):
                    text = self.font.render(
                        '(' + str(
                            np.round(
                                coord_v[index]
                                @ self.get_animation_step(),
                                decimals=2,
                            )[:3]
                        )[1:-1] + ')',
                        True,
                        pg.Color("white" if self.render.setting["bg_color"] == "black" else "black"),
                    )
                    self.render.screen.blit(text, vertex)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)


class Axis(Object3D):
    def __init__(
        self,
        render,
        # vertices,
        # faces,
        transformation=np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        ),
        animation=np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        ),
    ):
        self.vertices = np.array(
            [(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]
        )
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        super().__init__(
            render,
            vertices=self.vertices,
            faces=self.faces,
            transformation=transformation,
            animation=animation,
        )

        self.colors = [pg.Color("red"), pg.Color("green"), pg.Color("blue")]
        self.color_faces = [
            (color, face) for color, face in zip(self.colors, self.faces)
        ]
        self.label = "XYZ"
