from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

courses = [
	{
		'id': 1,
		'name': 'Business Fundamentals',
		'shortDescription': 'This course will get you acquainted with busines',
		'price': 20.0
	},
	{
		'id': 2,
		'name': 'Math Fundamentals',
		'shortDescription': 'This course will get you acquainted with math',
		'price': 50.0
	},
	{
		'id': 3,
		'name': 'Programming Fundamentals',
		'shortDescription': 'This course will get you acquainted with programming',
		'price': 100500.0
	}
]

@app.route('/api/v1.0/courses', methods=['GET'])
def get_courses():
    return jsonify({'courses': courses});
	
@app.route('/api/v1.0/courses', methods=['POST'])
def create_course():
	if not request.json or not 'name' or not 'shortDescription':
		abort(400)
		
	if not request.json['price']:
		newPrice = 0.0
	else: 
		newPrice = request.json['price']
	
	course = {
		'id': courses[-1]['id'] + 1,
		'name': request.json['name'],
		'shortDescription': request.json['shortDescription'],
		'price': newPrice
	}
	
	courses.append(course);
	return jsonify({'course': course}), 201
	
@app.route('/api/v1.0/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
	course = next(filter(lambda course: course['id'] == course_id, courses), False)
	if not course:
		abort(404)
	return jsonify({'course': course})
	
@app.route('/api/v1.0/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
	course = next(filter(lambda course: course['id'] == course_id, courses), False)
	if not course:
		abort(404)
	if not request.json or not 'name' or not 'shortDescription':
		abort(400)
	course['name'] = request.json['name']
	course['shortDescription'] = request.json['shortDescription']
	if (request.json['price']):
		course['price'] = request.json['price']
	return jsonify({'course': course})
	
@app.route('/api/v1.0/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
	course = next(filter(lambda course: course['id'] == course_id, courses), False)
	if not course:
		abort(404)
	courses.remove(course)
	return jsonify({'result': True})
	
	
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404);

if __name__ == '__main__':
    app.run(debug=True)