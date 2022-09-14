from visdom import Visdom
import numpy as np

viz = Visdom()
textwindow= viz.text("Hello")
image_window = viz.image(
    np.random.rand(3,256,256),
    opts=dict(
        tiltle = "random",
        caption = "random noise"
    )
)