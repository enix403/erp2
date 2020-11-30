import React from 'react';

// import "flatpickr/dist/themes/light.css";
// import DateInput from '../../components/dateinput';

import './index.css';
import CellDialoge from './celldialogue';
import TimeTable from './table';
import LectureDialog from './lecturedialog';

window.facultyData = window.SERVER_DATA.staffs;
window.subjectsData = window.SERVER_DATA.subjects;
window.tableData = window.SERVER_DATA.table_data;


// window.tableData = {
//     lectures: [0, 0, 0, 0, 0, 0, 0],
//     lectureTimes: [
//         [
//             '12:00 AM - 12:00 AM', 
//             '12:00 AM - 12:00 AM',
//             '12:43 AM - 12:00 AM',
//             '12:00 AM - 12:00 AM',
//             '12:00 AM - 12:00 AM',
//             '12:00 AM - 12:00 AM',
//             '12:00 AM - 12:00 AM',
//         ]
//     ],
//     sections: [
//         {
//             id: 1,
//             name: "PMG45",
//             cells: [
//                 {
//                     lectureIndex: 0,
//                     fragments: [
//                         {
//                             ranges: [[1, 3]],
//                             facultyId: 3,
//                             subjectId: 1
//                         },
//                         {
//                             ranges: [[4, 6]],
//                             facultyId: 2,
//                             subjectId: 3
//                         },
//                     ]
//                 },
//             ]
//         }
//     ]
// };



class MainTableView extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            cellModelOpen: false,
            lectureModelOpen: false,
            activeCell: { sectionId: null, lectureIndex: null }
        };

        this.daysLookup = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
        }
    }

    handleClose = () => { 
        this.setState({ cellModelOpen: false, activeCell: {sectionId: null, lectureIndex: null}});
    };

    handleCellClick = (_lectureIndex, _sectionId) => {
        this.setState({
            cellModelOpen: true,
            activeCell: {
                sectionId: _sectionId,
                lectureIndex: _lectureIndex
            }
        });
    };

    render() {

        return (
            <React.Fragment>
                <button 
                    class="bp3-button bp3-small bp3-outlined bp3-intent-primary bp3-icon-add mb-md"
                    onClick={() => this.setState({lectureModelOpen: true})}
                >
                    Edit Lectures
                </button>
                <CellDialoge
                    open={this.state.cellModelOpen}
                    onClose={this.handleClose}
                    activeCell={this.state.activeCell}

                    daysLookup={this.daysLookup}

                />
                <LectureDialog open={this.state.lectureModelOpen} onClose={() => this.setState({lectureModelOpen: false})} />
                <TimeTable 
                    onCellClick={this.handleCellClick}
                    daysLookup={this.daysLookup}
                />
            </React.Fragment>
        );
    }
}


function App() {

    return (
        <React.Fragment>
            {/* <h6 className="bp3-heading">{window.SERVER_DATA.college.name} TimeTable</h6> */}
            <div className="table-responsive mt-md">
                <MainTableView />
            </div>
        </React.Fragment>
    );
}

export default App;