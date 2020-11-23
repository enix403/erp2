$(function () {
	$(".table-day").on("click", function (e) {
		e.preventDefault();

		$(".table-day.active").removeClass("active");
		$(this).addClass("active");

		$(".time-table").attr("hide", "");
		let target = $($(this).attr("href"));
		target.removeAttr("hide");
	});

	$(".create_table").on("click", function (e) {
		// e.preventDefault();

		let row_template = $("#lecture_row_template").clone();
		row_template.removeAttr("hide");
		row_template.removeAttr("id");

		let form = $(this).parents(".create_table_form");
		// lecture_rows_card

		let num_lectures = +form.find(".table_num_lectures").val();
		form.attr("data-num-lectures", num_lectures);
		// console.log(num_lectures);

		form.find(".lecture_rows_card").removeAttr("hide");

		form.find(".lecture_rows_container").empty();

		for (let i = 0; i < num_lectures; i++) {
			let row = row_template.clone();
			row.find(".t_slot_num").html(`Slot ${i + 1}`);
			row.attr("data-slot-num", i + 1);
			form.find(".lecture_rows_container").append(row);
		}
	});

	$(".go-slots-btn").on("click", function () {
		let form = $(this).parents(".create_table_form");
		let num_lectures = +form.attr("data-num-lectures");

		// console.log(num_lectures);

		let current_lecture_num = 0;

		let slots = [];

		for (let i = 0; i < num_lectures; i++) {
			let row = form.find(`.slot_row[data-slot-num=${i + 1}]`);

			let l_type = +row.find(".l_type").val();

			let slot_payload = {};
			// if (l_type == 1) {
				// normal
				// current_lecture_num++;
				// slot_payload["ui_number"] = current_lecture_num;
			// } else {
				// slot_payload["ui_number"] = 0;
			// }

			slot_payload['order'] = i;
			slot_payload["l_type"] = l_type;
			slot_payload["time_start"] = row.find(".time_start").val();
			slot_payload["time_end"] = row.find(".time_end").val();
			// slot_payload["lecture_number"] = i;

			slots.push(slot_payload);
		}
		// console.log(slots);

		let college_id = +$(".meta-input[name=college_id]").val();
		let week_day_server = +form.attr("data-day");
		let token = $(".meta-input[name=_token]").val();

		let payload = {
			csrfmiddlewaretoken: token,
			college_id,
			week_day: week_day_server,
			slots_json: JSON.stringify(slots),
		};

		let destination = $(".meta-input[name=create_table_link]").val();

		// console.log(slots);

		$.redirect(destination, payload, "POST");
	});

	// $('.create_table').trigger('click');
});
