import React from 'react';

class TimeTable extends React.Component {

    LECTURE_NORMAL = 0;
    LECTURE_BREAK = 1;

    constructor(props) {
        super(props);

        this.lectureCount = this.props.tableData.lectures.length;
    }

    shouldComponentUpdate() {
        return false;
    }

    makeLectureHeaders() {
        let headers = [];
        const lectures = this.props.tableData.lectures;

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



    _constructCell(cell) {

        if (!cell.fragments || cell.fragments.length == 0) {
            return "Empty";
        }


        return (
            <React.Fragment>

                {cell.fragments.map((frag, i) => {
                    return (
                        <React.Fragment key={i}>
                            <span
                                className="bp3-tag bp3-minimal bp3-intent-primary mr-tag"
                            >
                                {frag.start}-{frag.end}:
                            </span>
                            {frag.faculty} ({frag.subject})
                            <br />
                        </React.Fragment>
                    );
                })}
            </React.Fragment>
        );

    }

    constructCellsRowMarkup(cells) {
        let cellsRow = [];

        const cellsSorted = cells.concat().sort((c1, c2) => c1.lectureIndex > c2.lectureIndex);

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

        console.log("In TimeTable render()");

        const { lectureTimes, sections } = this.props.tableData;

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