from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum
from core.libs import assertions

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    filtered_assignments = [assignment for assignment in assignments if assignment.state in ['SUBMITTED', 'GRADED']]
    assignments_dump = AssignmentSchema().dump(filtered_assignments, many=True)
    return APIResponse.respond(data=assignments_dump)



@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    
    assertions.assert_found(assignment, 'No assignment with this id was found')

    if p.teacher_id != assignment.teacher_id:
        return jsonify({'error': 'FyleError', 'message': 'assigned to different teacher'}), 400

    if assignment.state not in [AssignmentStateEnum.SUBMITTED]:
        return jsonify({'error': 'FyleError', 'message': 'only a submitted assignment can be graded'}), 400

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)




