import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
import osuparser.beatmapparser as bp
import osuparser.utils as utils
import osuparser.slidercalc as slidercalc
import io
from copy import copy
import PIL
import numpy as np

# Render Beatmap as a PIL image
class BeatmapRenderer:
    def __init__(self, beatmap, window = None):
        self.beatmap = beatmap
        
        self.cs = float(self.beatmap["CircleSize"])
        self.ar = float(self.beatmap["ApproachRate"])
        
        self.radius = utils.cs_to_radius(self.cs)
        self.window = utils.ar_to_time(self.ar)[0]
        self.line_width = 1.0
    
    def render(self, offset, window = None):
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        self.ax.axis('off')
        canvas = FigureCanvasAgg(self.fig)
        
        plt.xlim([-160, 640])
        plt.ylim([460, -140])

        if window == None:
            window = self.window
        
        visible_objs = []
        for obj in self.beatmap["hitObjects"]:
            if (offset - window <= obj["startTime"] <= offset + window):
                visible_objs.append(obj)
        self.draw_objects(visible_objs, offset)
        
        canvas.draw()
        img = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
        
        plt.close(self.fig)

        return img
        
    def get_alpha(self, time):
        return utils.remain_time_to_opacity(self.ar, time)

    def draw_circle(self, obj):
        assert obj["object_name"] == "circle"
        circle = plt.Circle((obj["position"][0], obj["position"][1]), self.radius,
            fc='white', ec="black", linewidth=self.line_width)
        
        return [circle]

    def draw_slider(self, obj):
        assert obj["object_name"] == "slider"
        head = plt.Circle((obj["position"][0], obj["position"][1]), self.radius,
            fc='white', ec="black", linewidth=self.line_width)
        tail = plt.Circle((obj["end_position"][0], obj["end_position"][1]), self.radius,
            fc='white', ec="black", linewidth=self.line_width)
                  
        #vertices = self.get_slider_boundary(obj)
        
        #path1 = matplotlib.path.Path(vertices[0])
        #path2 = matplotlib.path.Path(vertices[1])
        #patch1 = matplotlib.patches.PathPatch(path1, ec='black', linewidth=self.line_width)
        #patch2 = matplotlib.patches.PathPatch(path2, ec='black', linewidth=self.line_width)
        
        patches = [] #[head, tail, patch1, patch2]
        for i in reversed(range(obj["pixelLength"])):
            pt = slidercalc.get_end_point(obj["curveType"], i, obj["points"])
            circle = plt.Circle((pt[0], pt[1]), self.radius,
                fc='white', ec="black", linewidth=self.line_width)
            patches.append(circle)
        
        return patches
        
    def draw_spinner(self, obj):
        pass
        
    def draw_objects(self, objs, offset):
        last_obj = None
        for obj in reversed(objs):
            alpha = self.get_alpha(offset - obj["startTime"])
            patches = []
            if obj["render_cache"] is None:
                # check object type and draw it
                if obj["object_name"] == "circle":
                    patches = self.draw_circle(obj)
                elif obj["object_name"] == "slider":
                    patches = self.draw_slider(obj)
                obj["render_cache"] = patches
            else: 
                patches = obj["render_cache"]
                
            for patch in patches:
                patch.set_alpha(alpha)
                self.ax.add_patch(copy(patch))
            
            if obj["newCombo"] == 0:
                if last_obj is not None:
                    end_pos = obj["end_position"] if obj["object_name"] == "slider" else obj["position"]
                    begin_pose = last_obj["position"]
                    begin = slidercalc.point_on_line(last_pos, obj["position"], self.radius / 2.0)
                    end = slidercalc.point_on_line(last_pos, obj["position"], slidercalc.distance - self.radius / 2.0)
                    path = matplotlib.path.Path([begin, end])
                    patch = matplotlib.patches.PathPatch(path, alpha=alpha)
                    self.ax.add_patch(patch)
                    
            # fig.text(240.0, 180.0, '1')
            
def make_pattern_beatmap(objs, cs=4):
    # make beatmap object from object list
    pass

if __name__ == "__main__":
    parser = bp.BeatmapParser()
    parser.parseFile("../../data/fazz.osu")
    beatmap = parser.build_beatmap()
    renderer = BeatmapRenderer(beatmap)
    
    import cv2, os
    tmp_file = "tmp.mp4"
    output_file = "test.mp4"
    videodims = (640, 480)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(tmp_file, fourcc, 60, videodims)

    for i in range(160):
        img = renderer.render(6500 + i * 16)
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        print("Finished processing {}".format(i), end = '\r')
        
    video.release()
    os.system("ffmpeg -y -i {} -vcodec libx264 -f mp4 {}".format(tmp_file, output_file))
    os.remove(tmp_file)