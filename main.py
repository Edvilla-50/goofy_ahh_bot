import discord, os, asyncio  # Added asyncio
alejandro = {}
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('hello goofy ahh'):
		await message.channel.send('hello, but dont call me that')

		# Wait for the next message from the same author
		def check(m):
			return m.author == message.author and m.channel == message.channel

		try:
			# Wait for "I'm sorry" or "Shut Up" after "Hello" response
			next_message = await client.wait_for('message', check=check, timeout=30.0)  # Timeout can be adjusted

			if next_message.content.startswith("I'm sorry"):
				await message.channel.send('I forgive you')
			elif next_message.content.startswith('Shut Up'):
				await message.channel.send('no')
		except asyncio.TimeoutError:
			await message.channel.send("Idiot")
	if message.content.startswith('Good Night goofy ahh'):
		un = message.author.name
		await message.channel.send(f'Good Night {un} stop calling me that though')
	if message.content.startswith('what am I lisenting too?'):
		user = message.author
		if user.activities:
			for activity in user.activities:
				if isinstance(activity, discord.Spotify):
					song = activity.title
					artist = activity.artist
					album = activity.album
					duration = activity.duration
					
					await message.channel.send(f'You are listening to {song} by {artist} from the album {album}')
		else:
			await message.channel.send('You are not listening to anything')






	#use dictionary to minecraft places as key and tuples of (x,y,z) as value
	if message.content.startswith('/commands'):
		await message.channel.send('1. /add \n 2. /print_all \n 3. /remove \n 4. /print_specific')
	#store location and cords
	if message.content.startswith('/add'):
		await message.channel.send('Enter place of interest')
		
		def check(m):
			return m.author == message.author and m.channel == message.channel
		try:
			response1 = await client.wait_for('message', check=check, timeout=30.0)
			await message.channel.send('Enter x cord')
			response2 = await client.wait_for('message', check=check, timeout=30.0)
			await message.channel.send('Enter y cord')
			response3 = await client.wait_for('message', check=check, timeout=30.0)
			await message.channel.send('Enter z cord')
			response4 = await client.wait_for('message', check=check, timeout=30.0)
			tup = (response2.content, response3.content, response4.content)
			if response1.content in alejandro:
				alejandro[response1.content].append(tup)
				await message.channel.send('Added')
			else:
				alejandro[response1.content] = [tup]
				await message.channel.send('Place added')
		except aiohttp.ClientError:
			await message.channel.send("You took too long to respond!")
	if message.content.startswith('/print_all'):
		if alejandro:
			all_places = '\n'.join([f'{place}: {cords}' for place, cords in alejandro.items()])
			await message.channel.send(f"stored places: \n {all_places}")
		else:
			await message.channel.send('No places added yet')
	if message.content.startswith('/remove'):
		await message.channel.send('Enter place of interest')
		def check(m):
			return m.author == message.author and m.channel == message.channel
		try:
			response1 = await client.wait_for('message', check=check, timeout=30.0)
			if response1.content in alejandro:
				alejandro.pop(response1.content)
				await message.channel.send('Place removed')
			else:
				await message.channel.send('Place not found')
		except asyncio.TimeoutError:
			await message.channel.send("You took too long to respond!")
	if message.content.startswith('/print_specific'):
		await message.channel.send('Enter place of interest')
		def check (m):
			return m.author == message.author and m.channel == message.channel
		try:
			response1  = await client.wait_for('message', check=check, timeout=30.0)
			if response1.content in alejandro:
				cords = alejandro[response1.content]
				await message.channel.send(f'{response1.content}: {cords}')
			else:
				await message.channel.send('Place not found')
		except asyncio.TimeoutError:
			await message.channel.send("You took too long to respond!")
			
		

try:
	client.run(os.getenv("TOKEN"))
except Exception as err:
	raise err