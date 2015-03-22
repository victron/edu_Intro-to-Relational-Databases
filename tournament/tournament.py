#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM match_results;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) from players;")
    results = cursor.fetchall()
    db.close()
    return results[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("insert into players (name) Values (%s)", (name,))
    db.commit()
    db.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
#    cursor.execute("select players.id,  players.name, coalesce(sum(matches.win),0)  as score_sum, count(matches.id) "
#                   "from players  left join matches on players.id = matches.id "
#                   "group by players.id order by score_sum desc")
    cursor.execute("select players.id, players.name, "
                   "count((select match_results.winner from match_results where match_results.winner = players.id)) as win, "
                   "count(match_results.winner ) as games "
                   "from players  left join match_results on "
                   "players.id= match_results.winner or players.id = match_results.loser  group by players.id")
    results = cursor.fetchall()
    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
#    cursor.execute("INSERT INTO matches (id, win) VALUES ((%s),1)", (winner,))
#    cursor.execute("INSERT INTO matches (id, win) VALUES ((%s),0)", (loser,))
    cursor.execute("INSERT INTO match_results (winner, loser) VALUES ((%s), (%s))", (winner, loser))
    db.commit()
    db.close()
    return
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("create view state as "
                   "select players.id as id, players.name, "
                   "count( (select match_results.winner from match_results where match_results.winner = players.id) ) as win, "
                   "count(match_results.winner ) as games "
                   "from players  left join match_results on players.id= match_results.winner or players.id = match_results.loser  "
                   "group by players.id")
    db.commit()
    cursor.execute("select state_a.id, state_a.name, state_b.id, state_b.name "
                   "from state as state_a, state as state_b "
                   "where state_a.win = state_b.win and state_a.id > state_b.id")
    results = cursor.fetchall()
    cursor.execute("DROP VIEW state")
    db.commit()
    db.close()
    return results



