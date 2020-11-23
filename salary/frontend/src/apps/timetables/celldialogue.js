import React from 'react';
import { Dialog } from "@blueprintjs/core";


// class CellFragmentStore {
//     constructor() {
//         this.fragments = [];

//         this.items = {};

//         this.currentItemCount = 0
//     }

//     clear = () => {
//         this.fragments.length = 0;
//     };

// }

class CellFragment extends React.Component {
    render() {
        return (
            <div className="row">
                <div className="col-md-6">
                    <label className="bp3-label">
                        From
                        <div className="bp3-select bp3-fill">
                            <select onChange={(event) => this.props.onInput('from_day', event.target.value)}>
                                <option value="1">Monday</option>
                                <option value="2">Tuesday</option>
                                <option value="3">Wednesday</option>
                                <option value="4">Thursday</option>
                                <option value="5">Friday</option>
                                <option value="6">Saturday</option>
                            </select>
                        </div>
                    </label>

                    <label className="bp3-label">
                        To
                        <div className="bp3-select bp3-fill">
                            <select>
                                <option value="1">Monday</option>
                                <option value="2">Tuesday</option>
                                <option value="3">Wednesday</option>
                                <option value="4">Thursday</option>
                                <option value="5">Friday</option>
                                <option value="6">Saturday</option>
                            </select>
                        </div>
                    </label>

                </div>

                <div className="col-md-6">
                    <label className="bp3-label">
                        Faculty
                        <div className="bp3-select bp3-fill">
                            <select>
                                <option value="1">ABC</option>
                                <option value="2">XYZ</option>
                                <option value="3">ABC2</option>
                                <option value="4">PQR</option>
                            </select>
                        </div>
                    </label>

                    <label className="bp3-label">
                        Subject
                                    <div className="bp3-select bp3-fill">
                            <select>
                                <option value="1">Physics</option>
                                <option value="2">English</option>
                                <option value="3">Urdu</option>
                                <option value="4">Islamiat</option>
                                <option value="5">Chemistry</option>
                                <option value="6">Mathematics</option>
                            </select>
                        </div>
                    </label>

                </div>
            </div>
        );
    }
}


class CellDialoge extends React.Component {

    // constructor(props) {
    // super(props);

    // this.state = {
    // fragmentsData: this.props.initialFragments,
    // nextIndex: 0
    // }
    // }

    // _getEmptyFragment() {
    //     return {
    //         start: 1,
    //         end: 1,
    //         faculty: void (0),
    //         subject: void (0)
    //     }
    // }

    // addFragment = () => {
    //     const fragIndex = this.state.nextIndex;
    //     this.setState({
    //         fragmentsData: {
    //             ...this.state.fragmentsData,
    //             [fragIndex]: this._getEmptyFragment()
    //         },
    //         nextIndex: fragIndex + 1
    //     });
    // };


    render() {
        return (
            <Dialog
                style={{
                    width: '55vw'
                }}

                icon="flow-branch"
                transitionDuration={0}

                onClose={this.props.onClose}
                title="Edit Cell"
                autoFocus={true}
                canEscapeKeyClose={false}
                canOutsideClickClose={false}
                enforceFocus={true}
                usePortal={true}
                isOpen={this.props.open}
            >
                <div className="bp3-dialog-body">

                    <CellFragment
                        onInput={(fieldName, value) => this.props.onInput(1, fieldName, value)}
                    />
                    
                    {/* <h6 className="bp3-heading mb-sm">Range:</h6> */}
                    {/* <CellFragment /> */}
                    {/* <h6 className="bp3-heading mb-sm">Range:</h6> */}
                    {/* <CellFragment /> */}

                </div>
                <div className="bp3-dialog-footer">

                    <div className="bp3-dialog-footer-actions">
                        <button
                            className="bp3-button bp3-minimal bp3-intent-danger"
                            onClick={this.props.onClose}
                        >
                            <span className="bp3-button-text">Cancel</span>
                        </button>

                        <button
                            className="bp3-button bp3-outlined bp3-intent-success"
                            onClick={this.props.onSave}

                        >
                            <span className="bp3-button-text">Save Cell</span>
                        </button>

                    </div>
                </div>
            </Dialog>
        );
    }
}

export default CellDialoge;