

import React from 'react';

// import './index.css';
import "flatpickr/dist/themes/light.css";

import DateInput from '../../components/dateinput';
// import Dialog from '@blueprintjs/core/lib/esm/components/dialog/dialog';

// import { AnchorButton, Button, Classes, Code, Dialog, H5, Intent, Switch, Tooltip } from "@blueprintjs/core";
// import {  Classes, Dialog } from "@blueprintjs/core";
// import { POSITION_TOP } from '@blueprintjs/core/lib/esm/common/classes';


class TransferForm extends React.Component {

    constructor(props) {
        super(props)

        this.colleges = window.SERVER_DATA.colleges;

        this.state = {
            transferDate: undefined,
            sourceCollegeIndex: this.colleges.length > 0 ? 0 : -1,
        };

    }


    handleCollegeChange = (event) => {

        const selectedCollegeId = event.target.value;
        let newCollegeIndex = -1;

        for (let i = 0; i < this.colleges.length; i++) {
            const clg = this.colleges[i];
            if (clg.id == selectedCollegeId) {
                newCollegeIndex = i;
                break;
            }
        }


        this.setState({ sourceCollegeIndex: newCollegeIndex });
    };


    render() {

        const selectedCollege = this.state.sourceCollegeIndex > -1 && this.colleges[this.state.sourceCollegeIndex];


        return (
            <React.Fragment>
                <div className="col-md-6 mb-md">
                    <label className="bp3-label">
                        Source College
                        <div className="bp3-select bp3-fill">
                            <select
                                onChange={this.handleCollegeChange}
                                name="source_college_id"
                            >
                                {this.colleges.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                            </select>
                        </div>
                    </label>

                    <label className="bp3-label">
                        Staff to transfer
                        <div className="bp3-select bp3-fill">
                            <select name="staff_id">
                                {
                                    !!selectedCollege && selectedCollege.staffs.map(s => {
                                        return <option key={s.id} value={s.id}>{s.name}</option>;
                                    })
                                }
                            </select>
                        </div>
                    </label>


                    <label className="bp3-label">
                        With Effect From
                        <DateInput
                            value={this.state.transferDate}
                            onChange={new_date => {
                                this.setState({ transferDate: new_date });
                            }}
                            serverName="transfer_date"
                        />
                    </label>


                </div>
                <div className="col-md-6 mb-md">
                    <label className="bp3-label">
                        Destination College
                        <div className="bp3-select bp3-fill">
                            <select name="dest_college_id">
                                {
                                    this.colleges.map(c => {
                                        if (c.id == selectedCollege.id) {
                                            return false;
                                        }
                                        return <option key={c.id} value={c.id}>{c.name}</option>
                                    })
                                }
                            </select>
                        </div>
                    </label>

                    <button className="bp3-button bp3-outlined bp3-intent-success">
                        <span className="bp3-button-text">Transfer</span>
                        <span className="bp3-icon bp3-icon-changes"></span>
                    </button>

                </div>
            </React.Fragment>
        );
    }
}

function TransferApp() {

    return (
        <React.Fragment>
            <h6 className="bp3-heading">Transfer Staff</h6>
            <div className="row mt-md">
                <TransferForm />

            </div>
        </React.Fragment>
    );
}
/*
class TransferAppMain extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            autoFocus: true,
            canEscapeKeyClose: false,
            canOutsideClickClose: false,
            enforceFocus: true,
            isOpen: false,
            usePortal: true,
        };

        // window.openme = () => {this.setState({isOpen: true})};

    }

    handleClose = () => this.setState({ isOpen: false });

    render() {

        return (
            <Dialog
                // className={this.props.data.themeName}

                style={{
                    width: '50%'
                }}

                icon="flow-branch"
                transitionDuration={0}

                onClose={this.handleClose}
                title="Palantir Foundry"
                {...this.state}
            >
                <div className={Classes.DIALOG_BODY}>
                    <TransferApp />
                </div>
                <div className={Classes.DIALOG_FOOTER}>
                    <div className={Classes.DIALOG_FOOTER_ACTIONS}>
                        <button className="bp3-button bp3-outline4d bp3-intent-success">
                            <span className="bp3-icon bp3-icon-changes"></span>
                            <span className="bp3-button-text">Transfer</span>
                        </button>

                    </div>
                </div>
            </Dialog>
        );
    }
}

*/
export default TransferApp;




