import glob
import moviepy.editor as mpy
gif_name = 'ford_fulkerson_method'
fps = 1
file_list = glob.glob('ford_fulkerson_method/frames/*')
file_list.sort(key= lambda file_name: int(file_name[29:-4]))
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('ford_fulkerson_method/{}.gif'.format(gif_name), fps=fps)