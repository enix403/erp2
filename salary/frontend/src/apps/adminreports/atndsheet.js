import React from 'react';

import { Button } from '@blueprintjs/core/lib/esm/components/button/buttons';
import { Intent } from '@blueprintjs/core/lib/esm/common/intent';
// import { InputGroup } from '@blueprintjs/core/lib/esm/components/forms/inputGroup';


import DateInput from '../../components/dateinput';


class AtndSheetForm extends React.Component {


    constructor(props) {
        super(props)

        this.state = {
            date_start: undefined,
            date_end: undefined,
        };

        this.colleges = window.SERVER_DATA.colleges;
        this.college_hidden_input = false;
        if (window.SERVER_DATA.college_fixed) {
            this.college_hidden_input = <input type="hidden" name="college_id" value={this.colleges[0].id} />
        }
    }


    render() {

        return (

            <form  action={window.SERVER_DATA.urls.atndsheet} method="GET">
                {this.college_hidden_input}

                <br />

                
                <label className="bp3-label">
                    College
                    <div className="bp3-select bp3-fill">
                        <select disabled={window.SERVER_DATA.college_fixed} name="college_id">
                            {this.colleges.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                        </select>
                    </div>
                </label>


                <label className="bp3-label">
                    Staff Type
                    <div className="bp3-select bp3-fill">
                        <select name="type">
                            <option value="0">Faculty</option>
                            <option value="1">Administration</option>
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
                    intent={Intent.SUCCESS}
                    minimal={true}
                    outlined={true}
                />

            </form>
        );
    }
};


export default AtndSheetForm;
