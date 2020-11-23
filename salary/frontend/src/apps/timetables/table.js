import React from 'react';

// array[Math.floor(Math.random() * array.length)];
const allIntents = ['danger', 'warning', 'success', 'primary'];
// const allIntents = ['danger'];

function getRandomIntent() {
    return allIntents[Math.floor(Math.random() * allIntents.length)];
}



class TimeTable extends React.Component {

    LECTURE_NORMAL = 0;
    LECTURE_BREAK = 1;

    constructor(props) {
        super(props);

        this.lectureCount = window.tableData.lectures.length;
        this.daysLookup = this.props.daysLookup;

        this.subjectsLookup = {};
        for (let i = 0; i < window.subjectsData.length; i++) {
            const subject = window.subjectsData[i];
            this.subjectsLookup[subject.id] = subject;
        }

        this.facultyLookup = {};
        for (let i = 0; i < window.facultyData.length; i++) {
            const faculty = window.facultyData[i];
            this.facultyLookup[faculty.id] = faculty;
        }
    }

    shouldComponentUpdate() {
        return false;
    }

    makeLectureHeaders() {
        let headers = [];
        const lectures = window.tableData.lectures;

        for (let i = 0, w = 1; i < lectures.length; i++) {
            const lec = lectures[i];
            if (lec == this.LECTURE_BREAK) {
                headers.push("Break")
            }
            else {
                headers.push(`Lecture ${w++}`);
            }
        }

        return headers;
    }

    
    _constructCellRepeatTag(ranges) {
        return ranges.map((range) => {
            // return "Everyday" instead of "Monday-Saturday"
            if (range[0] == 1 && range[1] == 6) {
                return 'Everyday';
            }
            return `${this.daysLookup[range[0]]}-${this.daysLookup[range[1]]}`;
        }).join(',') + ':';
    }


    _constructCell(cell) {

        if (!cell.fragments || cell.fragments.length == 0) {
            return "Empty";
        }


        return (
            <>
                {cell.fragments.map((frag, i) => {
                    return (
                        <React.Fragment key={i}>
                            <span
                                className={`bp3-tag bp3-minimal bp3-intent-${getRandomIntent()} mr-tag`}
                            >
                                {this._constructCellRepeatTag(frag.ranges)}
                            </span>
                            {this.facultyLookup[frag.facultyId].name} ({this.subjectsLookup[frag.subjectId].name})
                            <br />
                        </React.Fragment>
                    );
                })}
            </>
        );

    }

    constructCellsRowMarkup(cells) {

        let cellsRow = [];

        const cellsSorted = cells.concat().sort((c1, c2) => c1.lectureIndex - c2.lectureIndex);

        let targetLectureIndex = 0;
        let i = 0;
        while (i < cellsSorted.length) {

            let currentCell = cellsSorted[i];
            while (targetLectureIndex < currentCell.lectureIndex) {
                cellsRow.push(
                    {
                        lectureIndex: targetLectureIndex,
                        markup: "N/A"
                    }
                );
                targetLectureIndex++;
            }

            // cellsRow.push(this._constructCell(currentCell));
            cellsRow.push(
                {
                    lectureIndex: currentCell.lectureIndex,
                    markup: this._constructCell(currentCell)
                }
            );

            i++;
            targetLectureIndex++;
        }

        while (targetLectureIndex < this.lectureCount) {

            // cellsRow.push("N/A");
            cellsRow.push(
                {
                    lectureIndex: targetLectureIndex,
                    markup: "N/A"
                }
            );
            targetLectureIndex++;
        }



        return cellsRow;
    }


    render() {

        const { lectureTimes, sections } = window.tableData;

        return (
            <table className="table table-sm table-bordered center-table">
                <thead>
                    <tr>
                        <th>Section</th>
                        {this.makeLectureHeaders().map((h, i) => {
                            return <th key={i}>{h}</th>;
                        })}

                    </tr>

                    <tr>
                        {lectureTimes.map((row, i) => {
                            return (
                                <React.Fragment key={i}>
                                    <th></th>
                                    {row.map((t, j) => {
                                        return (
                                            <th key={j}><small><strong>{t}</strong></small></th>
                                        );
                                    })}
                                </React.Fragment>
                            );
                        })}
                    </tr>

                </thead>

                <tbody>

                    {sections.map(section => {
                        return (
                            <tr key={section.id}>
                                <th>{section.name}</th>
                                {this.constructCellsRowMarkup(section.cells).map(result => {
                                    return (
                                        <td
                                            key={result.lectureIndex}
                                            className="tbl-cell"
                                            onClick={
                                                () => this.props.onCellClick(result.lectureIndex, section.id)
                                            }
                                        >
                                            {result.markup}
                                        </td>
                                    )
                                })}
                            </tr>
                        );
                    })}

                </tbody>

            </table>
        );
    }
}

export default TimeTable;