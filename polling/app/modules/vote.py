from flask import Flask, request, jsonify
from datetime import datetime
from bson.objectid import ObjectId
from collections import Counter

# Modelo de votação
class Poll:
    def __init__(self, title, question, options, correct_answer, start_time, end_time, type_poll, anonymous=True):
        self.title = title
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.start_time = start_time
        self.end_time = end_time
        self.type_poll = type_poll
        self.anonymous = anonymous
        self.ballots = []

    def add_ballot(self, ranked_options):
        self.ballots.append(ranked_options)

def create_poll(db, request):
    data = request.json
    title = data['title']
    question = data['question']
    options = data['options']
    correct_answer = data['correct_answer'] if data['type_poll'] == 'for_correct_answer' else None
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
    type_poll = data['type_poll']
    anonymous = data.get('anonymous', True)

    poll = Poll(title, question, options, correct_answer, start_time, end_time, type_poll, anonymous)

    db.polls.insert_one(poll.__dict__)

    return jsonify({"message": "Poll created successfully"})


def vote(db, request):
    data = request.json
    poll_id = data['poll_id']
    ranked_options = data['ranked_options']

    poll = db.polls.find_one({"_id": ObjectId(poll_id)})
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    if datetime.now() < poll['start_time'] or datetime.now() > poll['end_time']:
        return jsonify({"error": "Voting period has ended"}), 400

    if len(ranked_options) != len(set(ranked_options)):
        return jsonify({"error": "Duplicate options in the ranking"}), 400

    poll_obj = Poll(poll['title'], poll['question'], poll['options'], poll['correct_answer'], 
                    poll['start_time'], poll['end_time'], poll['type_poll'], poll['anonymous'])
    poll_obj.add_ballot(ranked_options)

    db.votes.insert_one({"poll_id": poll_id, "ballot": ranked_options})

    return jsonify({"message": "Vote submitted successfully"})


def get_results_polls(db, request):
    data = request.json
    poll_id = data['poll_id']
    poll = db.polls.find_one({"_id": ObjectId(poll_id)})
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    if datetime.now() < poll['end_time']:
        return jsonify({"error": "Voting period has not ended yet"}), 400

    poll_obj = Poll(poll['title'], poll['question'], poll['options'], poll['correct_answer'], 
                    poll['start_time'], poll['end_time'], poll['type_poll'], poll['anonymous'])
    
    vote_list = []

    for vote in db.votes.find({"poll_id": poll_id}):
        if poll['type_poll'] == 'for_correct_answer':
            poll_obj.add_ballot(vote['ballot'])
        else:
            vote_list.append(vote['ballot'][0])

    if poll['type_poll'] == 'for_correct_answer':
        results = {option: poll_obj.ballots.count(option) for option in poll_obj.options}
    else:
        total_votes = len(vote_list)
        votes_counts = Counter(vote_list)

        results = {"poll_id": poll_id, "type_poll" : poll['type_poll'], "question" : poll['question']}
        for votes, count in votes_counts.items():
            results[votes] = round((count / total_votes) * 100,2)
    
    return jsonify(results)

