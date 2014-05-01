from PIL import Image
import numpy
import subprocess as sp
import random
import os

FFMPEG_BIN = 'ffmpeg.exe'
command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f','image2pipe',
        '-vcodec','mjpeg',
        '-s', '1280x720', # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '24', # frames per second
        '-i', '-', # The imput comes from a pipe
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'mpeg4',
        '-b', '2000k', # bitrate
        'my_output_videofile.mp4' ]

def bg_draw(bg_im,frame,speed,pipe):
	bg_width,bg_height = bg_im.size
	out_im = Image.new(mode ='RGB',size=(1280,720),color = 0)
	bg_offset = -(int(frame*bg_width/(24*speed)) % bg_width)
	out_im.paste(bg_im,(bg_offset,0))
	if (bg_width + bg_offset) < 1280:
		out_im.paste(bg_im,(bg_width + bg_offset,0))
	return out_im

class BgTree(object):
	"""tree objects that will move in the background. at every interation, they should drawSelf() and nextFrame"""
	trees = []
	def __init__(self,tree_im):
		self.coordinates = 1280
		self.tree_im = tree_im
		self.trees.append(self)
	def nextFrame(self):
		self.coordinates += -7
		if self.coordinates < -500:
			del self

class TelephonePole(object):
	"""Telephone pole objects that will move in the background. at every interation, they should drawSelf() and nextFrame"""
	poles = []
	def __init__(self,pole_im):
		self.coordinates = 1280
		self.pole_im = pole_im
		self.poles.append(self)
	def nextFrame(self):
		self.coordinates += -10
		if self.coordinates < -500:
			del self

class BirdsObj(object):
	"""Telephone pole objects that will move in the background. at every interation, they should drawSelf() and nextFrame"""
	birds = []
	def __init__(self,bird_im,vert_coord):
		self.coordinates = 1280
		self.vert_coord = vert_coord
		self.bird_im = bird_im
		self.birds.append(self)
	def nextFrame(self):
		self.coordinates += -10
		if self.coordinates < -100:
			del self

class Wires(object):
	"""Telephone wire objects that will move in the background. at every interation, they should drawSelf() and nextFrame"""
	wires = []
	def __init__(self,wires_im):
		self.coordinates = 1280
		self.wires_im = wires_im
		self.wires.append(self)
	def nextFrame(self):
		self.coordinates += -10
		if self.coordinates < -3000:
			del self

def wireData(wiredata_im):
	wire_array = numpy.asarray(wiredata_im)
	height,width,__ = wire_array.shape
	output_data = numpy.zeros([width+1,6])
	for column in xrange(width):
		transcheck = True
		transcounter = 0
		wire_num = -1
		for row in xrange(height):
			if transcheck and transcounter > 5:
				wire_num += 1
				transcheck = False
				transcounter = 0

			if transcheck and wire_array[row][column][3] < 200:
				transcounter += 1

			elif (not transcheck) and wire_array[row][column][3] > 50:
				transcheck = True
				output_data[column][wire_num] = row

			if wire_num > 5:
				break
	return output_data



def main():
	pipe = sp.Popen(command, stdin=sp.PIPE, stderr=None)	#create pipe. set stderr to None because otherwise it would take up too much memory
	total_frames = 5200
	bg_im = Image.open('image_assets/cloud_loop2.png')
	polename = 'image_assets/poles_wires/pole1.png'
	wiresname = 'image_assets/poles_wires/wires12.png'
	tree_list = [0] *total_frames
	w_data_12 = wireData(Image.open('image_assets/poles_wires/wires12_data.png'))
	w_data_21 = wireData(Image.open('image_assets/poles_wires/wires21_data.png'))
	w_data = w_data_21

	#song data goes below. input FRAME NUMBER:[List of wires with birds] as a dict
	note_data = {264:[3], 283:[1], 300:[2], 318:[3], 337:[6], 356:[7], 375:[6], 394:[5], 414:[8],
				 469:[10], 490:[10,5], 547:[10,6], 606:[10,5], 665:[10,6],
				 726:[3], 744:[1], 762:[2], 782:[3], 800:[6], 821:[7], 840:[6], 860:[6], 879:[8],
				 900:[10,6], 939:[6], 958:[10,6], 997:[3], 1022:[10,5],
				 1059:[11], 1084:[7,9], 1142:[9,5], 1204:[10,8],
				 1243:[8], 1262:[7], 1281:[6], 1301:[4], 1321:[5], 1339:[7], 1359:[5], 1379:[6], 1399:[7], 1421:[5],
				 1532:[5], 1551:[4], 1571:[3], 1590:[2], 1612:[1], 1635:[6], 1654:[5], 1675:[4], 1697:[5], 1719:[7], 1740:[5],
				 1850:[5], 1876:[2], 1944:[3], 2002:[7], 2023:[8], 2043:[7], 2061:[6], 2081:[5], 2101:[4], 2122:[6], 2144:[5], 2165:[4],
				 2190:[10], 2214:[8,5], 2237:[9,7],
				 2267:[11,8,6], 2333:[10,8,5],
				 2422:[10,5], 2490:[10,6], 2557:[10,5], 2626:[10,6],
				 2694:[3], 2715:[1], 2735:[2], 2755:[3], 2774:[6], 2795:[7], 2815:[6], 2836:[5], 2858:[8],
				 2918:[10], 2941:[10,5], 3005:[10,6], 3068:[10,5], 3132:[10,6],
				 3193:[3], 3213:[1], 3231:[2], 3251:[3], 3270:[6], 3291:[7], 3312:[6], 3334:[5], 3357:[8],
				 3416:[6], 3479:[3], 3540:[11],
				 3725:[8], 3745:[7], 3764:[6], 3785:[4], 3804:[5], 3825:[7], 3846:[5], 3867:[6], 3889:[7], 3912:[5],
				 4023:[5], 4044:[4], 4064:[3], 4084:[2], 4106:[1], 4128:[6], 4149:[5], 4168:[4], 4189:[5], 4212:[7], 4234:[5],
				 4351:[5], 4379:[2], 4447:[3 ], 4511:[7], 4532:[6], 4553:[3], 4574:[4], 4597:[5], 4617:[6], 4644:[4], 4673:[5], 4697:[6],
				 4727:[10], 4758:[8,5], 4788:[9,5],
				 4829:[11,8,6], 4922:[10,8,5] }

	for i in xrange(total_frames):
		#random seeding (heh) of trees
		if numpy.random.ranf() < 0.005:
			tree_list[i] = 1

	treecount = 0
	birdcount_e = 0
	birdcount_f = 0

	for i in xrange(total_frames):
		print i
		current_frame = bg_draw(bg_im,i,100,pipe)
		if tree_list[i] == 1:
			#create a tree 
			tree_file = 'image_assets/trees/treen' + str(treecount%7) + '.png'
			treecount += 1
			tree_im = Image.open(tree_file)
			tree = BgTree(tree_im)

		if i == 0 or (i % 250 == 0):
			pole_im = Image.open(polename)
			wires_im = Image.open(wiresname)
			if polename == 'image_assets/poles_wires/pole1.png':
				polename = 'image_assets/poles_wires/pole2.png'
				wiresname = 'image_assets/poles_wires/wires21.png'
				w_data = w_data_12
			else:
				polename = 'image_assets/poles_wires/pole1.png'
				wiresname = 'image_assets/poles_wires/wires12.png'
				w_data = w_data_21
			pole = TelephonePole(pole_im)
			wire = Wires(wires_im)


		if note_data.get(i,0):
			for note in note_data.get(i,0):
				if note % 2 == 0:
					bird_im = Image.open('image_assets/birds/birdf_' + str(birdcount_f%5) +'.png')
					bird = BirdsObj(bird_im,w_data[(i%250)*10][int(note/2)]-100)
					birdcount_f += 1
				else:
					bird_im = Image.open('image_assets/birds/birde_' + str(birdcount_e%5) +'.png')
					bird = BirdsObj(bird_im,w_data[(i%250)*10][int(note/2)]-100)
					birdcount_e += 1

		for treeobj in BgTree.trees:
			#draw all trees and propagate them to their next frames
			current_frame.paste(treeobj.tree_im,(treeobj.coordinates,100),treeobj.tree_im)
			treeobj.nextFrame()
		for poleobj in TelephonePole.poles:
			current_frame.paste(poleobj.pole_im,(poleobj.coordinates,0),poleobj.pole_im)
			poleobj.nextFrame()
		for wiresobj in Wires.wires:
			current_frame.paste(wiresobj.wires_im,(wiresobj.coordinates,0),wiresobj.wires_im)
			wiresobj.nextFrame()
		for birdobj in BirdsObj.birds:
			current_frame.paste(birdobj.bird_im,(int(birdobj.coordinates),int(birdobj.vert_coord)),birdobj.bird_im)
			birdobj.nextFrame()
		current_frame.save(pipe.stdin,'jpeg')

	pipe.stdin.close()
	pipe.wait()

if __name__ == "__main__":
	main()