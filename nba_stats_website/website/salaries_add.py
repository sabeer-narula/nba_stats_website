import csv

def add_salary_column(player_stats_file, salaries_data):
    # Read the player stats from the CSV file
    with open(player_stats_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        player_stats = list(reader)

    # Create a dictionary to store player salaries
    player_salaries = {}
    for line in salaries_data.split('\n'):
        if line.strip():
            parts = line.rsplit(',', 1)
            name = parts[0].strip().split(' ', 1)[1].strip()  # Extract the player name
            salary = parts[-1].strip().replace('$', '').replace(',', '')
            player_salaries[name] = salary

    # Add the 'SALARY' column to the headers
    headers.append('SALARY')

    # Add the salary to each player's data
    updated_player_stats = []
    for player in player_stats:
        player_name = player[headers.index('PLAYER_NAME')]
        salary = player_salaries.get(player_name, '')
        player.append(salary)
        updated_player_stats.append(player)

    # Write the updated player stats back to the 'normalized_player_stats.csv' file
    with open(player_stats_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(updated_player_stats)

# Provide the file paths and salaries data
player_stats_file = 'normalized_player_stats.csv'
output_file = 'updated_player_stats.csv'
salaries_data = '''
1Stephen Curry, PGGolden State Warriors$51,915,615
2Kevin Durant, PFPhoenix Suns$47,649,433
3LeBron James, SFLos Angeles Lakers$47,607,350
4Nikola Jokic, CDenver Nuggets$47,607,350
5Joel Embiid, CPhiladelphia 76ers$46,900,000
6Bradley Beal, SGPhoenix Suns$46,741,590
7Giannis Antetokounmpo, PFMilwaukee Bucks$45,640,084
8Damian Lillard, PGMilwaukee Bucks$45,640,084
9Kawhi Leonard, SFLA Clippers$45,640,084
10Paul George, FLA Clippers$45,640,084
11Jimmy Butler, SFMiami Heat$45,183,960
12Klay Thompson, SGGolden State Warriors$43,219,440
13Rudy Gobert, CMinnesota Timberwolves$41,000,000
14Fred VanVleet, PGHouston Rockets$40,806,300
15Anthony Davis, PFLos Angeles Lakers$40,600,080
16Luka Doncic, PGDallas Mavericks$40,064,220
17Zach LaVine, SGChicago Bulls$40,064,220
18Trae Young, PGAtlanta Hawks$40,064,220
19Tobias Harris, PFPhiladelphia 76ers$39,270,150
20Ben Simmons, PGBrooklyn Nets$37,893,408
21Pascal Siakam, PFIndiana Pacers$37,893,408
22Kyrie Irving, PGDallas Mavericks$37,037,037
23Jrue Holiday, PGBoston Celtics$36,861,707
24Devin Booker, SGPhoenix Suns$36,016,200
25Karl-Anthony Towns, CMinnesota Timberwolves$36,016,200
26Kristaps Porzingis, CBoston Celtics$36,016,200
27CJ McCollum, SGNew Orleans Pelicans$35,802,469
28James Harden, SGLA Clippers$35,640,000
29Ja Morant, PGMemphis Grizzlies$34,005,250
30Darius Garland, PGCleveland Cavaliers$34,005,250
31Zion Williamson, PFNew Orleans Pelicans$34,005,250
32Jamal Murray, PGDenver Nuggets$33,833,400
33Brandon Ingram, SFNew Orleans Pelicans$33,833,400
34Shai Gilgeous-Alexander, PGOklahoma City Thunder$33,386,850
35Michael Porter Jr., SFDenver Nuggets$33,386,850
36Donovan Mitchell, SGCleveland Cavaliers$33,162,030
37De'Aaron Fox, PGSacramento Kings$32,600,060
38Bam Adebayo, CMiami Heat$32,600,060
39Jayson Tatum, SFBoston Celtics$32,600,060
40Deandre Ayton, CPortland Trail Blazers$32,459,438
41Jaylen Brown, SGBoston Celtics$31,830,357
42Gordon Hayward, SFOklahoma City Thunder$31,500,000
43Chris Paul, PGGolden State Warriors$30,800,000
44Domantas Sabonis, PFSacramento Kings$30,600,000
45Khris Middleton, SFMilwaukee Bucks$29,320,988
46DeMar DeRozan, SFChicago Bulls$28,600,000
47Julius Randle, PFNew York Knicks$28,226,880
48Jordan Poole, SGWashington Wizards$27,955,357
49Jerami Grant, SFPortland Trail Blazers$27,586,207
50Jaren Jackson Jr., PFMemphis Grizzlies$27,102,202
51Tyler Herro, PGMiami Heat$27,000,000
52Jalen Brunson, PGNew York Knicks$26,346,666
53Cameron Johnson, SFBrooklyn Nets$25,679,348
54Kyle Kuzma, SFWashington Wizards$25,568,182
55John Collins, PFUtah Jazz$25,340,000
56Brook Lopez, CMilwaukee Bucks$25,000,000
57Mike Conley, PGMinnesota Timberwolves$24,360,000
58Andrew Wiggins, SFGolden State Warriors$24,330,357
59Anfernee Simons, SGPortland Trail Blazers$24,107,143
60RJ Barrett, SGToronto Raptors$23,883,929
61Jordan Clarkson, PGUtah Jazz$23,487,629
62Dillon Brooks, SFHouston Rockets$22,627,671
63Malcolm Brogdon, PGPortland Trail Blazers$22,500,000
64Draymond Green, PFGolden State Warriors$22,321,429
65Aaron Gordon, PFDenver Nuggets$22,266,182
66Terry Rozier, SGMiami Heat$22,205,221
67Bruce Brown, SFToronto Raptors$22,000,000
68Mikal Bridges, SFBrooklyn Nets$21,700,000
69Myles Turner, CIndiana Pacers$20,975,000
70Clint Capela, CAtlanta Hawks$20,616,000
71Lonzo Ball, PGChicago Bulls$20,465,117
72De'Andre Hunter, SFAtlanta Hawks$20,089,286
73Keldon Johnson, SFSan Antonio Spurs$20,000,000
74Bojan Bogdanovic, SFNew York Knicks$20,000,000
75Jarrett Allen, CCleveland Cavaliers$20,000,000
76Joe Harris, SFDetroit Pistons$19,928,571
77Jakob Poeltl, CToronto Raptors$19,500,000
78Buddy Hield, SGPhiladelphia 76ers$19,279,841
79Evan Fournier, SGDetroit Pistons$18,857,143
80Marcus Smart, PGMemphis Grizzlies$18,833,712
81Bogdan Bogdanovic, SGAtlanta Hawks$18,700,000
82OG Anunoby, SFNew York Knicks$18,642,857
83Gary Trent Jr., SGToronto Raptors$18,560,000
84Nikola Vucevic, CChicago Bulls$18,518,519
85Derrick White, PGBoston Celtics$18,357,143
86Dejounte Murray, SGAtlanta Hawks$18,214,000
87Duncan Robinson, FMiami Heat$18,154,000
88Norman Powell, GLA Clippers$18,000,000
89Tim Hardaway Jr., SFDallas Mavericks$17,897,728
90Jonathan Isaac, PFOrlando Magic$17,400,000
91Collin Sexton, PGUtah Jazz$17,325,000
92D'Angelo Russell, PGLos Angeles Lakers$17,307,693
93Lauri Markkanen, PFUtah Jazz$17,259,999
94Marcus Morris Sr., SFCleveland Cavaliers$17,116,279
95Davis Bertans, SFCharlotte Hornets$17,000,000
96Harrison Barnes, SFSacramento Kings$17,000,000
97Markelle Fultz, PGOrlando Magic$17,000,000
98Jusuf Nurkic, CPhoenix Suns$16,875,000
99P.J. Washington, PFDallas Mavericks$16,847,826
100Kevin Porter Jr., GOklahoma City Thunder$15,860,000
101Rui Hachimura, PFLos Angeles Lakers$15,740,741
102Mitchell Robinson, CNew York Knicks$15,681,818
103Kevin Huerter, SGSacramento Kings$15,669,643
104Jonas Valanciunas, CNew Orleans Pelicans$15,435,000
105Luke Kennard, SGMemphis Grizzlies$15,418,363
106Caris LeVert, SGCleveland Cavaliers$15,384,616
107Luguentz Dort, GOklahoma City Thunder$15,277,778
108Kentavious Caldwell-Pope, SGDenver Nuggets$14,704,938
109Max Strus, SGCleveland Cavaliers$14,487,684
110Tyus Jones, PGWashington Wizards$14,000,000
111Dorian Finney-Smith, PFBrooklyn Nets$13,932,008
112Doug McDermott, SFIndiana Pacers$13,750,000
113Wendell Carter Jr., COrlando Magic$13,050,000
114Gary Harris, SGOrlando Magic$13,000,000
115Josh Hart, SGNew York Knicks$12,960,000
116Naz Reid, CMinnesota Timberwolves$12,950,400
117Steven Adams, CHouston Rockets$12,600,000
118Brandon Clarke, PFMemphis Grizzlies$12,500,000
119Marvin Bagley III, PFWashington Wizards$12,500,000
120Dennis Schroder, PGBrooklyn Nets$12,405,000
121Daniel Gafford, CDallas Mavericks$12,402,000
122Grant Williams, PFCharlotte Hornets$12,325,581
123Kelly Olynyk, PFToronto Raptors$12,195,122
124Victor Wembanyama, CSan Antonio Spurs$12,160,680
125James Wiseman, CDetroit Pistons$12,119,400
126Devonte' Graham, PGSan Antonio Spurs$12,100,000
127Richaun Holmes, FWashington Wizards$12,046,020
128Austin Reaves, SGLos Angeles Lakers$12,015,150
129Herbert Jones, SFNew Orleans Pelicans$12,015,150
130Chris Boucher, PFToronto Raptors$11,750,000
131Nicolas Batum, PFPhiladelphia 76ers$11,710,818
132Bobby Portis, FMilwaukee Bucks$11,710,818
133Robert Covington, PFPhiladelphia 76ers$11,692,308
134Paolo Banchero, PFOrlando Magic$11,608,080
135Robert Williams III, CPortland Trail Blazers$11,571,429
136Coby White, PGChicago Bulls$11,111,111
137Cade Cunningham, PGDetroit Pistons$11,055,240
138Talen Horton-Tucker, SGUtah Jazz$11,020,000
139P.J. Tucker, PFLA Clippers$11,014,500
140Joe Ingles, SGOrlando Magic$11,000,000
141Maxi Kleber, PFDallas Mavericks$11,000,000
142Donte DiVincenzo, SGNew York Knicks$10,960,000
143Ivica Zubac, CLA Clippers$10,933,333
144LaMelo Ball, PGCharlotte Hornets$10,900,635
145Brandon Miller, FCharlotte Hornets$10,880,400
146Terance Mann, SGLA Clippers$10,576,923
147Matisse Thybulle, SGPortland Trail Blazers$10,500,000
148Gabe Vincent, PGLos Angeles Lakers$10,500,000
149Alec Burks, SGNew York Knicks$10,489,600
150Chet Holmgren, PFOklahoma City Thunder$10,386,000
151Larry Nance Jr., PFNew Orleans Pelicans$10,375,000
152Landry Shamet, SGWashington Wizards$10,250,000
153Al Horford, CBoston Celtics$10,000,000
'''


# Call the function to add the salary column
add_salary_column(player_stats_file, salaries_data)