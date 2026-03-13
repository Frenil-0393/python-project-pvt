from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from media.models import BroadcastSession, Highlight, PressRelease
from organizer.models import Match, PlayerStat, ScoreUpdate


DEMO_PASSWORD = "demo12345"


USER_FIXTURES = [
    {
        "username": "fan_demo",
        "first_name": "Aarav Fan",
        "email": "fan_demo@scoreclub.local",
        "role": "fan",
    },
    {
        "username": "organizer_demo",
        "first_name": "Nia Ops",
        "email": "organizer_demo@scoreclub.local",
        "role": "organizer",
    },
    {
        "username": "media_demo",
        "first_name": "Maya Broadcast",
        "email": "media_demo@scoreclub.local",
        "role": "media",
    },
]


MATCH_FIXTURES = [
    {
        "sport": "Cricket",
        "home_team": "Mumbai Meteors",
        "away_team": "Delhi Strikers",
        "venue": "National Oval",
        "start_offset_hours": -2,
        "status": Match.STATUS_LIVE,
    },
    {
        "sport": "Football",
        "home_team": "Bengaluru Titans",
        "away_team": "Goa Waves",
        "venue": "Harbor Arena",
        "start_offset_hours": -1,
        "status": Match.STATUS_LIVE,
    },
    {
        "sport": "Basketball",
        "home_team": "Pune Pulse",
        "away_team": "Hyderabad Rise",
        "venue": "SkyDome Center",
        "start_offset_hours": 5,
        "status": Match.STATUS_SCHEDULED,
    },
    {
        "sport": "Tennis",
        "home_team": "Riya Sen",
        "away_team": "Kavya Nair",
        "venue": "Center Court One",
        "start_offset_hours": 12,
        "status": Match.STATUS_SCHEDULED,
    },
    {
        "sport": "Kabaddi",
        "home_team": "Chennai Chargers",
        "away_team": "Surat Storm",
        "venue": "Metro Indoor Hall",
        "start_offset_hours": 20,
        "status": Match.STATUS_SCHEDULED,
    },
    {
        "sport": "Cricket",
        "home_team": "Jaipur Kings",
        "away_team": "Lucknow Falcons",
        "venue": "Royal Greens",
        "start_offset_hours": -30,
        "status": Match.STATUS_FINISHED,
    },
    {
        "sport": "Football",
        "home_team": "Kerala Force",
        "away_team": "Punjab Arrows",
        "venue": "South Stand Arena",
        "start_offset_hours": 28,
        "status": Match.STATUS_SCHEDULED,
    },
    {
        "sport": "Volleyball",
        "home_team": "Ahmedabad Spikes",
        "away_team": "Indore Blaze",
        "venue": "Velocity Court",
        "start_offset_hours": 34,
        "status": Match.STATUS_SCHEDULED,
    },
    {
        "sport": "Basketball",
        "home_team": "Nagpur Orbit",
        "away_team": "Kolkata Edge",
        "venue": "Summit Arena",
        "start_offset_hours": -18,
        "status": Match.STATUS_FINISHED,
    },
    {
        "sport": "Cricket",
        "home_team": "Rajasthan Blasters",
        "away_team": "Punjab Rockets",
        "venue": "Desert Field",
        "start_offset_hours": 42,
        "status": Match.STATUS_SCHEDULED,
    },
    {
        "sport": "Hockey",
        "home_team": "Odisha Blades",
        "away_team": "Mumbai Sticks",
        "venue": "Glide Dome",
        "start_offset_hours": 16,
        "status": Match.STATUS_SCHEDULED,
    },
    {
        "sport": "Football",
        "home_team": "Delhi Storm",
        "away_team": "Chennai Mariners",
        "venue": "Capital Park",
        "start_offset_hours": -3,
        "status": Match.STATUS_LIVE,
    },
    {
        "sport": "Badminton",
        "home_team": "Pranav Iyer",
        "away_team": "Rohan Das",
        "venue": "Court 9 Arena",
        "start_offset_hours": -22,
        "status": Match.STATUS_FINISHED,
    },
]


SCORE_FIXTURES = [
    ("Mumbai Meteors", "Delhi Strikers", "168/4 in 16.2 overs", "Powerplay recovery underway"),
    ("Mumbai Meteors", "Delhi Strikers", "191/6 in 19 overs", "Death overs pressure building"),
    ("Bengaluru Titans", "Goa Waves", "2 - 1", "78th minute | Titans pressing high"),
    ("Jaipur Kings", "Lucknow Falcons", "214/8", "Final score | Kings win by 11 runs"),
    ("Nagpur Orbit", "Kolkata Edge", "98 - 91", "Final score | Orbit close late with a 9-2 run"),
    ("Pune Pulse", "Hyderabad Rise", "74 - 68", "Third quarter | Pulse bench unit in control"),
    ("Delhi Storm", "Chennai Mariners", "1 - 1", "62nd minute | End-to-end transitions"),
    ("Nagpur Orbit", "Kolkata Edge", "105 - 99", "Final score | Orbit shut down late possessions"),
    ("Pranav Iyer", "Rohan Das", "2 - 0", "Final | 21-16, 21-18"),
]


PLAYER_FIXTURES = [
    ("Mumbai Meteors", "Delhi Strikers", "R. Sharma", "Mumbai Meteors", "Runs", "74", "Available"),
    ("Mumbai Meteors", "Delhi Strikers", "A. Khan", "Delhi Strikers", "Wickets", "3", "Available"),
    ("Bengaluru Titans", "Goa Waves", "L. Pereira", "Bengaluru Titans", "Goals", "2", "Starting XI"),
    ("Bengaluru Titans", "Goa Waves", "V. Dias", "Goa Waves", "Assists", "1", "Starting XI"),
    ("Jaipur Kings", "Lucknow Falcons", "S. Gill", "Jaipur Kings", "Runs", "92", "Available"),
    ("Pune Pulse", "Hyderabad Rise", "K. Thomas", "Pune Pulse", "Points", "28", "Probable"),
    ("Kerala Force", "Punjab Arrows", "A. Menon", "Kerala Force", "Goals", "9", "Available"),
    ("Ahmedabad Spikes", "Indore Blaze", "N. Verma", "Ahmedabad Spikes", "Aces", "14", "Available"),
    ("Nagpur Orbit", "Kolkata Edge", "J. Reed", "Nagpur Orbit", "Points", "31", "Available"),
    ("Delhi Storm", "Chennai Mariners", "M. Khan", "Delhi Storm", "Goals", "1", "Starting XI"),
    ("Delhi Storm", "Chennai Mariners", "A. Fernando", "Chennai Mariners", "Assists", "1", "Starting XI"),
    ("Odisha Blades", "Mumbai Sticks", "R. Tirkey", "Odisha Blades", "Goals", "12", "Available"),
    ("Pranav Iyer", "Rohan Das", "Pranav Iyer", "Independent", "Smashes", "27", "Available"),
]


HIGHLIGHT_FIXTURES = [
    (
        "Mumbai Meteors",
        "Delhi Strikers",
        "Meteor finishers ignite the death overs",
        "A late-over acceleration clip featuring sixes, pressure bowling, and a crowd-swinging finish.",
        "03:42",
        18420,
    ),
    (
        "Bengaluru Titans",
        "Goa Waves",
        "Titans flip the match with a two-minute press",
        "The midfield turnover and back-to-back chances that changed the tone of the second half.",
        "02:18",
        9650,
    ),
    (
        "Jaipur Kings",
        "Lucknow Falcons",
        "Final over drama closes out the chase",
        "A pressure sequence from the closing over with the winning reaction from the dugout.",
        "04:05",
        12730,
    ),
    (
        "Nagpur Orbit",
        "Kolkata Edge",
        "Orbit close the game with a fourth-quarter run",
        "Transition buckets and defensive stops seal a late comeback in the indoor arena.",
        "02:54",
        8420,
    ),
    (
        "Pune Pulse",
        "Hyderabad Rise",
        "Pulse second unit flips the tempo",
        "A fast-break sequence and corner shooting stretch the lead midway through the contest.",
        "03:08",
        6130,
    ),
    (
        "Delhi Storm",
        "Chennai Mariners",
        "Storm equalizer from a quick corner routine",
        "A compact build-up and near-post finish level the match in front of a loud home crowd.",
        "01:42",
        7340,
    ),
    (
        "Pranav Iyer",
        "Rohan Das",
        "Straight-set finish with baseline pressure",
        "Winner compilation from a two-game closeout featuring late rallies and net kills.",
        "02:11",
        4580,
    ),
    (
        "Mumbai Meteors",
        "Delhi Strikers",
        "Top 5 wicket moments | match recap",
        "Slow-motion wicket package cut for social clips and post-match analysis.",
        "04:32",
        11980,
    ),
]


BROADCAST_FIXTURES = [
    ("Mumbai Meteors", "Delhi Strikers", "Arena One HD", "https://stream.scoreclub.local/arena-one", True),
    ("Bengaluru Titans", "Goa Waves", "PitchView 4K", "https://stream.scoreclub.local/pitchview", True),
    ("Pune Pulse", "Hyderabad Rise", "Hoops Central", "https://stream.scoreclub.local/hoops-central", False),
    ("Kerala Force", "Punjab Arrows", "South Stand Live", "https://stream.scoreclub.local/south-stand", False),
    ("Ahmedabad Spikes", "Indore Blaze", "CourtVision Max", "https://stream.scoreclub.local/courtvision", False),
    ("Delhi Storm", "Chennai Mariners", "Derby Cam", "https://stream.scoreclub.local/derby-cam", True),
    ("Rajasthan Blasters", "Punjab Rockets", "Pitch Radar", "https://stream.scoreclub.local/pitch-radar", False),
    ("Odisha Blades", "Mumbai Sticks", "HockeyLine HD", "https://stream.scoreclub.local/hockeyline", False),
]


PRESS_FIXTURES = [
    (
        "Cricket",
        "Mumbai Meteors surge into the closing overs with momentum",
        "The Meteors entered the final stretch with attacking intent after a composed middle-order rebuild. Organizers confirmed strong fan turnout and a smooth operations window.",
        PressRelease.STATUS_PUBLISHED,
    ),
    (
        "Football",
        "Titans tactical press reshapes second half narrative",
        "Bengaluru's advanced press triggered a momentum swing late in the second half, with the media desk capturing key tactical sequences for post-match coverage.",
        PressRelease.STATUS_PUBLISHED,
    ),
    (
        "Basketball",
        "Pulse prepare rotation-heavy approach for primetime tipoff",
        "The upcoming contest is expected to feature deeper bench involvement, with organizers finalizing player-availability notes ahead of the evening slate.",
        PressRelease.STATUS_DRAFT,
    ),
    (
        "Volleyball",
        "Spikes and Blaze set for high-tempo net battle",
        "Both sides arrive with aggressive serving profiles, prompting media teams to prepare a more tactical pre-match segment for the evening show.",
        PressRelease.STATUS_DRAFT,
    ),
    (
        "Football",
        "Kerala Force confirm full-strength squad for weekend clash",
        "The organizer desk confirmed availability across the starting core ahead of the South Stand Arena fixture, with broadcast prep shifting into final checks.",
        PressRelease.STATUS_PUBLISHED,
    ),
    (
        "Football",
        "Delhi and Chennai trade momentum in high-intensity live fixture",
        "Both sides remain level in a transition-heavy contest, with production teams tracking tactical shape changes for in-match breakdown segments.",
        PressRelease.STATUS_PUBLISHED,
    ),
    (
        "Hockey",
        "Blades announce expanded training squad before weekend clash",
        "Team management shared an updated availability bulletin, while broadcast units finalized camera positions for the Glide Dome venue.",
        PressRelease.STATUS_DRAFT,
    ),
]


def _build_match_lookup():
    return {
        (match.home_team, match.away_team): match
        for match in Match.objects.all()
    }


def seed_demo_data():
    user_model = get_user_model()
    now = timezone.now().replace(minute=0, second=0, microsecond=0)

    created_users = 0
    for item in USER_FIXTURES:
        user, created = user_model.objects.get_or_create(
            username=item["username"],
            defaults={
                "first_name": item["first_name"],
                "email": item["email"],
                "role": item["role"],
            },
        )
        changed = created
        if user.first_name != item["first_name"]:
            user.first_name = item["first_name"]
            changed = True
        if user.email != item["email"]:
            user.email = item["email"]
            changed = True
        if user.role != item["role"]:
            user.role = item["role"]
            changed = True
        if created or not user.check_password(DEMO_PASSWORD):
            user.set_password(DEMO_PASSWORD)
            changed = True
        if changed:
            user.save()
        if created:
            created_users += 1

    created_matches = 0
    for item in MATCH_FIXTURES:
        match, created = Match.objects.update_or_create(
            sport=item["sport"],
            home_team=item["home_team"],
            away_team=item["away_team"],
            defaults={
                "venue": item["venue"],
                "start_time": now + timedelta(hours=item["start_offset_hours"]),
                "status": item["status"],
            },
        )
        if created:
            created_matches += 1

    match_lookup = _build_match_lookup()

    created_scores = 0
    for home_team, away_team, summary, status_note in SCORE_FIXTURES:
        match = match_lookup[(home_team, away_team)]
        _, created = ScoreUpdate.objects.get_or_create(
            match=match,
            summary=summary,
            defaults={"status_note": status_note},
        )
        if not created:
            ScoreUpdate.objects.filter(match=match, summary=summary).update(status_note=status_note)
        if created:
            created_scores += 1

    created_stats = 0
    for home_team, away_team, player_name, team_name, metric_name, metric_value, availability in PLAYER_FIXTURES:
        match = match_lookup[(home_team, away_team)]
        _, created = PlayerStat.objects.update_or_create(
            match=match,
            player_name=player_name,
            metric_name=metric_name,
            defaults={
                "team_name": team_name,
                "metric_value": metric_value,
                "availability": availability,
            },
        )
        if created:
            created_stats += 1

    created_highlights = 0
    for home_team, away_team, title, description, duration, views in HIGHLIGHT_FIXTURES:
        match = match_lookup[(home_team, away_team)]
        _, created = Highlight.objects.update_or_create(
            match=match,
            title=title,
            defaults={
                "description": description,
                "duration": duration,
                "views": views,
            },
        )
        if created:
            created_highlights += 1

    created_broadcasts = 0
    for home_team, away_team, channel_name, stream_url, is_live in BROADCAST_FIXTURES:
        match = match_lookup[(home_team, away_team)]
        _, created = BroadcastSession.objects.update_or_create(
            match=match,
            channel_name=channel_name,
            defaults={
                "stream_url": stream_url,
                "is_live": is_live,
            },
        )
        if created:
            created_broadcasts += 1

    created_press = 0
    for sport, headline, body, status in PRESS_FIXTURES:
        _, created = PressRelease.objects.update_or_create(
            headline=headline,
            defaults={
                "sport": sport,
                "body": body,
                "status": status,
            },
        )
        if created:
            created_press += 1

    return {
        "users": created_users,
        "matches": created_matches,
        "scores": created_scores,
        "stats": created_stats,
        "highlights": created_highlights,
        "broadcasts": created_broadcasts,
        "press": created_press,
        "password": DEMO_PASSWORD,
    }
