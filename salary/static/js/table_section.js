function make_payload() {
	let lectures_objs = [];
    

	$(".lecture_row").each(function () {
		let lecture_id = +$(this).data("lectureId");
		let faculty_id = +$(this).find(".fac_id").val();
		let subject_id = +$(this).find(".subject_id").val();

		let is_null = !!$(this).find(".lc_is_null").prop("checked");

		if (!is_null) {
			
			lectures_objs.push({
				lecture_id,
				faculty_param_id: faculty_id,
				subject_id,
			});
		}

		// lecture_id = $(this).find('')
	});

	return lectures_objs;
}

function send() {
	let lectures = make_payload()
	let lectures_json = JSON.stringify(lectures);

	let college_id = +$("[name=_meta__college_id]").val();
	let section_id = +$("[name=_meta__section_id]").val();
	let table_id = +$("[name=_meta__table_id]").val();
	

	let payload = {
		csrfmiddlewaretoken: TOKEN,

		college_id: college_id,
		section_id: section_id,
		table_id: table_id,

		lectures_json: lectures_json,
	};

	$.redirect(SEND_URL, payload, "POST");

}

let r = function () {
	function get_payload() {
		let url = new URL(window.location.href);

		// let num_lectures = +url.searchParams.get("num_lectures");
		let week_day = +url.searchParams.get("week_day");
		payload = {
			_token: TOKEN,
			section_id: +url.searchParams.get("section_id"),
			// num_lectures,
			week_day: +(week_day % 7), // to convert client sunday(7) to server sunday(0)
			lectures: JSON.stringify(calc_lectures()),
		};

		return payload;
	}

	function calc_lectures(week_day = null) {
		// let lectures = {};

		// for (let week_day = 1; week_day < 7; week_day++) {
		let day_lectures = [];

		$(".lecture_row").each(function () {
			let lecture_num = +$(this).attr("data-lecture-num");
			let lecture_data = {};
			let i = lecture_num;

			lecture_data["l_num"] = lecture_num;
			lecture_data["fac_id"] = +$(
				`#l_fac_${get_id_suffix(week_day, i)}`
			).val();
			lecture_data["subject_id"] = +$(
				`#l_subject_${get_id_suffix(week_day, i)}`
			).val();
			lecture_data["is_null"] = !!$(
				`#l_null_${get_id_suffix(week_day, i)}`
			).prop("checked");

			day_lectures[i] = lecture_data;
		});

		// for (let i = 0; i < num_lectures; i++) {

		// }

		return day_lectures;

		lectures[week_day] = day_lectures;
		// }

		// return lectures;
	}

	function send() {
		let payload = get_payload();
		$.redirect(SEND_URL, payload, "POST");
	}
};
