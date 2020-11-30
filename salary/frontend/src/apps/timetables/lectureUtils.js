export function getLectureName(index) {

    const lectures = window.tableData.lectures;

    for (let i = 0, w = 1; i < lectures.length; i++) {
        const lec = lectures[i];

        if (index == i) {
            if (lec == 1) {
                return "Break";
            }
            else {
                return `Lecture ${w}`;
            }
        }

        if (lec != 1) {
            w++;
        }
    }
}