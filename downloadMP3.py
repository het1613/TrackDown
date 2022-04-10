from pathlib import Path
import os
import yt_dlp
from youtube_search import YoutubeSearch
import multiprocessing

def downloadSongs(name, songs):
	TOTAL_ATTEMPS = 10
	SAVE_PATH = str(os.path.join(Path.home(), f"Downloads/{name}"))

	try:
		os.mkdir(SAVE_PATH)
	except:
		print("Downloads/Songs Folder Already Exists")
	
	for song in songs:
		attempts = 0
		best_url = None

		while attempts<TOTAL_ATTEMPS:

			try:
				results_list = YoutubeSearch(song, max_results=1).to_dict()
				best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
				break

			except IndexError:
				attempts_left += 1
				print("No valid URLs found for {}, trying again ({} attempts left).".format(song, attempts_left))
		
		if best_url is None:
			print("No valid URLs found for {}, skipping track.".format(song))
			continue
		
		print("\nInitiating download for {}.".format(song))
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
			'outtmpl': f"{SAVE_PATH}/{song}.%(ext)s",
		}
		
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download([best_url])

def multicoreDownloadSongs(name, songs, cpu_count):
	number_of_songs = len(songs)
	songs_per_cpu = number_of_songs // cpu_count
	extra_songs = number_of_songs % cpu_count

	# Allocate correct number of songs to each CPU
	# 4 cores and 6 songs = [2, 2, 1, 1]
	cpu_count_list = [songs_per_cpu]*cpu_count

	for cpu_index, cpu_songs in enumerate(cpu_count_list):
		if cpu_index<extra_songs:
			cpu_songs+=1
			cpu_count_list[cpu_index] = cpu_songs
	
	# Split up songs list into groups
	# Create 2D list of segments
	index = 0
	file_segments = []
	for cpu_songs in cpu_count_list:
		segment = songs[index:cpu_songs + index]
		index += cpu_songs
		file_segments.append(segment)

	# Prepare processes
	processes = []
	for segment in file_segments:
		p = multiprocessing.Process(target = downloadSongs, args=(name, segment,))
		processes.append(p)

    # Start the processes
	for p in processes:
		p.start()

    # Wait for the processes to complete and exit as a group
	for p in processes:
		p.join()

def ListToMP3(playlist_name, playlist_songs):
	print("Found ", len(playlist_songs), " songs!")

	available_cores = multiprocessing.cpu_count() - 2
	multicoreDownloadSongs(playlist_name, playlist_songs, available_cores)

# ListToMP3()