import React from 'react';

import { Button } from '@blueprintjs/core/lib/esm/components/button/buttons';
import { Intent } from '@blueprintjs/core/lib/esm/common/intent';

import DateInput from '../../components/dateinput';


class LectureSheetForm extends React.Component {

    constructor(props) {
        super(props)

        this.colleges = window.SERVER_DATA.colleges;

        this.state = {
            date_start: undefined,
            date_end: undefined,

            selectedCollegeIndex: this.colleges.length > 0 ? 0 : -1
        };

        this.collegeHiddenInput = false;
        if (window.SERVER_DATA.college_fixed) {
            this.collegeHiddenInput = <input type="hidden" name="college_id" value={this.colleges[0].id} />
        }
    }


    handleCollegeChange = (event) => {

        if (window.SERVER_DATA.college_fixed) {
            return;
        }


        const selectedCollegeId = event.target.value;
        let newCollegeIndex = -1;

        for (let i = 0; i < this.colleges.length; i++) {
            const clg = this.colleges[i];
            if (clg.id == selectedCollegeId) {
                newCollegeIndex = i;
                break;
            }
        }


        this.setState({ selectedCollegeIndex: newCollegeIndex });
    };


    render() {


        const selectedCollege = this.state.selectedCollegeIndex > -1 && this.colleges[this.state.selectedCollegeIndex];

        return (

            <form action={window.SERVER_DATA.urls.lecsheet} method="GET">
                {this.collegeHiddenInput}

                <br />

                <label className="bp3-label">
                    College
                    <div className="bp3-select bp3-fill">
                        <select
                            onChange={this.handleCollegeChange}
                            disabled={window.SERVER_DATA.college_fixed}
                            name="college_id"
                        >
                            {this.colleges.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                        </select>
                    </div>
                </label>



                <label className="bp3-label">
                    Faculty
                    <div className="bp3-select bp3-fill">
                        <select name="faculty_param_id">

                            {
                                !!selectedCollege && selectedCollege.faculty.length > 0 &&
                                <option value="-1">-- All --</option>
                            }

                            {
                                !!selectedCollege && selectedCollege.faculty.map(f => {
                                    return <option key={f.id} value={f.id}>{f.name}</option>;
                                })
                            }
                        </select>
                    </div>
                </label>


                <label className="bp3-label">
                    Start Date
                    <DateInput
                        value={this.state.date_start}
                        onChange={new_date => {
                            this.setState({ date_start: new_date });
                        }}
                        serverName="from"
                    />
                </label>


                <label className="bp3-label">
                    End Date
                    <DateInput
                        value={this.state.date_end}
                        onChange={new_date => {
                            this.setState({ date_end: new_date });
                        }}
                        serverName="to"
                    />
                </label>

                <br />

                <Button
                    type="submit"
                    text="Generate"
                    icon="build"
                    fill={true}
                    intent={Intent.DANGER}
                    minimal={true}
                    outlined={true}
                />

            </form>
        );
    }
};


export default LectureSheetForm;
