from datetime import datetime   # Used for date / time conversions
import regex

class Scraper:
    def parse_time(self, time_str): # Converts playtime / match_time to seconds
        format_str = ""                 
        if "h" in time_str:
            if "m" not in time_str:
                format_str = "%Hh %Ss"
            else:
                format_str = "%Hh %Mm %Ss"
        elif "m" in time_str:
            format_str = "%Mm %Ss"
        else:
            format_str = "%Ss" 
        
        time_obj = datetime.strptime(time_str, format_str)                  # Convert the time into a datetime object
        delta_time = (time_obj - datetime(1900, 1, 1)).total_seconds()      # Convert the datetime object into seconds
        return int(delta_time)

    def get_usernames(self, source):
        return regex.findall("(?<=:arrow_down: |:arrow_down_small: |:trophy::arrow_up_small: |:trophy::arrow_up: |:arrow_double_down: |:trophy::arrow_double_up: |:regional_indicator_o: ).*?(?= [[])", str(source))

    def get_playtimes(self, source):
        return regex.findall("(?<=\w [[]).*?(?=[]])", str(source))
    
    def get_ratings(self, source):
        return regex.findall("(?<=]: ).*?(?= [-+]|\W)", str(source)) 

    def get_delta_ratings(self, source):
        return regex.findall("(?<= )[-+]\d.*?(?=\\n|\W)", str(source))

    def get_winners(self, match):
        field = match["embeds"][0]["description"]
        rating_change = []
        players = []

        usernames = self.get_usernames(field)
        playtimes = self.get_playtimes(field)
        rating = self.get_ratings(field + ".")
        delta_ratings = self.get_delta_ratings(field + ".")

        for i in range(0, len(usernames)):
            rating_change.append(int(delta_ratings[i]) if len(delta_ratings) > 0 else 0)

            player = {
                "username":         usernames[i],
                "new_rating":       int(rating[i]) + rating_change[i],
                "rating_change":    rating_change[i],
                "playtime":         self.parse_time(playtimes[i])
            }
            players.append(player)

        team = {
            "name":     match["embeds"][0]["author"]["name"],
            "won":      True,
            "players":  players
        }

        return [team]

    def get_losers(self, match):
        teams = []
        for field in match["embeds"][0]["fields"]:
            if "small_red_triangle_down" in field["name"]:
                players = []
                rating_change = []

                usernames = self.get_usernames(field)
                playtimes = self.get_playtimes(field)
                rating = self.get_ratings(field)
                delta_ratings = self.get_delta_ratings(field)
                
                for i in range(0, len(usernames)):
                    rating_change.append(int(delta_ratings[i]) if len(delta_ratings) > 0 else 0)
                    
                    try:
                        player = {
                            "username":         usernames[i],
                            "new_rating":       int(rating[i]) + rating_change[i],
                            "rating_change":    rating_change[i],
                            "playtime":         self.parse_time(playtimes[i])
                        }
                        players.append(player)
                    except Exception as e:
                        print("Caught Exception: ", e)
                        print("Source: ", field)


                team = {
                    "name":     field["name"].replace(":small_red_triangle_down: ", ''),
                    "won":      False,
                    "players":  players
                }
                teams.append(team)
            return teams

    def scrape(self, matches):
        parsed_matches = []
        for match in matches:
            embed_fields = match["embeds"][0]["fields"]
            match_type = embed_fields[len(embed_fields)-1]["value"]
            match_time = embed_fields[len(embed_fields)-2]["value"].replace(":clock10: ", '')
            
            try:
                date = datetime.strptime(match["timestamp"], '%Y-%m-%dT%H:%M:%S+00:00')
            except:
                date = datetime.strptime(match["timestamp"], '%Y-%m-%dT%H:%M:%S.%f+00:00')

            match_type = {
                "team": True if "Team" in match_type else False,
                "vip": False if "Rated" in match_type else True
            }

            match_data = {
                "_id": match["id"],
                "date": date,
                "match_time": self.parse_time(match_time),
                "match_type": match_type
            }

            match_data["teams"] = self.get_winners(match) + self.get_losers(match)
            parsed_matches.append(match_data)
        return parsed_matches