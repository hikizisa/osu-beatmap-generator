import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import osuparser.beatmapparser as bp
import osuparser.utils as utils
import io
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
    
    def render(self, offset, window = None):
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        self.ax.axis('off')
        canvas = FigureCanvasAgg(self.fig)
        
        plt.xlim([-160, 640])
        plt.ylim([-140, 460])

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

    def draw_circle(self, obj, alpha):
        assert obj["object_name"] == "circle"
        circle = plt.Circle((obj["position"][0], obj["position"][1]), self.radius,
            fc='white', ec="black", linewidth=4, alpha=alpha)
        self.ax.add_patch(circle)
        
    def draw_slider_boundary(self, obj):
        pass

    def draw_slider(self, obj):
        pass
        
    def draw_spinner(self, obj):
        pass
        
    def draw_objects(self, objs, offset):
        for obj in objs:
            alpha = self.get_alpha(offset - obj["startTime"])
            if obj["object_name"] == "circle":
                self.draw_circle(obj, alpha)
            # check object type and draw it
            
def make_pattern_beatmap(objs, cs=4):
    # make beatmap object from object list
    pass

if __name__ == "__main__":
    parser = bp.BeatmapParser()
    parser.parseFile("../../data/fazz.osu")
    beatmap = parser.build_beatmap()
    renderer = BeatmapRenderer(beatmap)
    
    import cv2
    videodims = (640, 480)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')    
    video = cv2.VideoWriter("test.mp4", fourcc, 60, videodims)

    for i in range(200):
        img = renderer.render(beatmap["hitObjects"][20]["startTime"] + i * 16)
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        
    video.release()
    