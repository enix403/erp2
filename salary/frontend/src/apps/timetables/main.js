import React from 'react';

// import "flatpickr/dist/themes/light.css";
// import DateInput from '../../components/dateinput';

import './index.css';
import CellDialoge from './celldialogue';
import TimeTable from './table';


// const __data = {

//     subjects: [
//         {
//             id: 1,
//             name: 'Maths'
//         }
//     ],

//     faculty: [
//         {
//             id: 1,
//             name: 'ABC'
//         }
//     ],


//     timetable: {
//         lectures: [0, 0, 0, 0, 1, 0, 0, 0],
//         sections: [
//             {
//                 id: 1,
//                 name: 'PMG2',
//                 cells: [
//                     {
//                         lecture_index: 0,
//                         fragments: [
//                             {
//                                 start_day: 1,
//                                 end_day: 4,
//                                 faculty: 1,
//                                 subject: 1
//                             }
//                         ]
//                     }
//                 ]
//             }
//         ]
//     }
// }


const tableData = {
    lectures: [0, 0, 0, 0, 0, 0, 0],
    lectureTimes: [
        [
            '12:00 AM - 12:00 AM', 
            '12:00 AM - 12:00 AM',
            '12:43 AM - 12:00 AM',
            '12:00 AM - 12:00 AM',
            '12:00 AM - 12:00 AM',
            '12:00 AM - 12:00 AM',
            '12:00 AM - 12:00 AM',
        ]
    ],
    sections: [
        {
            id: 1,
            name: "PMG45",
            cells: [
                {
                    lectureIndex: 0,
                    fragments: [
                        {
                            start: "Monday",
                            end: "Wednesday",
                            faculty: "Mr ABC",
                            subject: "English"
                        },
                        {
                            start: "Thursday",
                            end: "Saturday",
                            faculty: "Mr XYZ",
                            subject: "Maths"
                        }

                    ] 
                },
                {
                    lectureIndex: 1,
                    fragments: [
                        {
                            start: "Monday",
                            end: "Wednesday",
                            faculty: "Mr ABC",
                            subject: "English"
                        },
                        {
                            start: "Thursday",
                            end: "Saturday",
                            faculty: "Mr XYZ",
                            subject: "Maths"
                        }

                    ] 
                },
                {
                    lectureIndex: 2,
                    fragments: [
                        {
                            start: "Monday",
                            end: "Wednesday",
                            faculty: "Mr ABC",
                            subject: "English"
                        },
                        {
                            start: "Thursday",
                            end: "Saturday",
                            faculty: "Mr XYZ",
                            subject: "Maths"
                        }

                    ] 
                },
                {
                    lectureIndex: 3,
                    fragments: [
                        {
                            start: "Monday",
                            end: "Wednesday",
                            faculty: "Mr ABC",
                            subject: "English"
                        },
                        {
                            start: "Thursday",
                            end: "Saturday",
                            faculty: "Mr XYZ",
                            subject: "Maths"
                        }

                    ] 
                },
                {
                    lectureIndex: 4,
                    fragments: [
                        {
                            start: "Monday",
                            end: "Wednesday",
                            faculty: "Mr ABC",
                            subject: "English"
                        },
                        {
                            start: "Thursday",
                            end: "Saturday",
                            faculty: "Mr XYZ",
                            subject: "Maths"
                        }

                    ] 
                },
                {
                    lectureIndex: 5,
                    fragments: [
                        {
                            start: "Monday",
                            end: "Wednesday",
                            faculty: "Mr ABC",
                            subject: "English"
                        },
                        {
                            start: "Thursday",
                            end: "Saturday",
                            faculty: "Mr XYZ",
                            subject: "Maths"
                        }

                    ] 
                },
                {
                    lectureIndex: 6,
                    fragments: [
                        {
                            start: "Monday",
                            end: "Wednesday",
                            faculty: "Mr ABC",
                            subject: "English"
                        },
                        {
                            start: "Thursday",
                            end: "Saturday",
                            faculty: "Mr XYZ",
                            subject: "Maths"
                        }

                    ] 
                },
                
            ]
        }
    ]
};



class MainTableView extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            modelOpen: false,
            fragmentsData: {
                1: {}
            },
            nextIndex: []
        };
    }

    handleClose = () => { 
        this.setState({ modelOpen: false, initialSelectedFragments: [] })
    };

    handleSave = (_payload) => {
        this.handleClose();
    };

    handleInput = (fragmentIndex, fieldName, value) => {
        // const index = this.state.nextIndex;

        console.log(`New Value for ${fieldName} is ${value}`);

        this.setState({
            fragmentsData: {
                ...this.state.fragmentsData,
                [fragmentIndex]: {
                    ...this.state.fragmentsData[fragmentIndex],
                    [fieldName]: value
                }
            },
            // nextIndex: index + 1
        });
    };

    handleCellClick = (_lectureIndex, _sectionId) => {
        // TODO: fill initialSelectedFragments with values
        this.setState({ modelOpen: true });
    };

    render() {

        return (
            <React.Fragment>
                <CellDialoge
                    open={this.state.modelOpen}
                    onClose={this.handleClose}
                    onSave={this.handleSave}
                    initialFragments={[]}
                    onInput={this.handleInput}
                />
                <TimeTable 
                    onCellClick={this.handleCellClick}
                    tableData={tableData}
                />
            </React.Fragment>
        );
    }
}


function App() {

    return (
        <React.Fragment>
            <h6 className="bp3-heading">Fresh TimeTables</h6>
            <div className="table-responsive mt-md">
                <MainTableView />
            </div>
        </React.Fragment>
    );
}

export default App;