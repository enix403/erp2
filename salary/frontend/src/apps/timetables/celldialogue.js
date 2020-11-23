import React from 'react';
import { Dialog } from "@blueprintjs/core";


function WeekdayInput({ onChange, value }) {
    return (
        <select onChange={onChange} value={value}>
            <option value="1">Monday</option>
            <option value="2">Tuesday</option>
            <option value="3">Wednesday</option>
            <option value="4">Thursday</option>
            <option value="5">Friday</option>
            <option value="6">Saturday</option>
        </select>
    );
}

function FacultyInput({ onChange, value }) {
    return (
        <select onChange={onChange} value={value}>
            {window.facultyData.map((fac) => {
                return <option key={fac.id} value={fac.id}>{fac.name}</option>
            })}
        </select>
    );
}

function SubjectInput({ facultyId, onChange, value }) {

    const faculty = window.facultyData.find(fac => fac.id == facultyId);
    let allowedSubjects = [];
    if (faculty) {
        allowedSubjects = faculty.allowedSubjects;
    }

    return (
        <select onChange={onChange} value={value}>
            {window.subjectsData.map((sub) => {
                if (allowedSubjects.indexOf(sub.id) == -1) {
                    return false;
                }
                return <option key={sub.id} value={sub.id}>{sub.name}</option>;
            })}
        </select>
    );
}


function CellFragmentRange({ from, to, onStartChange, onEndChange }) {
    return (
        <div className="row row-sm">
            <div className="col-md-6">
                <label className="bp3-label">
                    From
                    <div className="bp3-select bp3-fill">
                        <WeekdayInput
                            value={from}
                            onChange={e => { onStartChange(e.target.value) }}
                        />
                    </div>
                </label>
            </div>
            <div className="col-md-6">

                <label className="bp3-label">
                    To
                    <div className="bp3-select bp3-fill">
                        <WeekdayInput
                            value={to}
                            onChange={e => { onEndChange(e.target.value) }}
                        />
                    </div>
                </label>

            </div>
        </div>
    );
}



function redirectUrl(path, params, method = 'post') {


    const form = document.createElement('form');
    form.method = method;
    form.action = path;

    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}



class CellFragment extends React.Component {
    render() {

        const frag = this.props.data;

        return (
            <div>
                <div className="row row-sm">

                    <div className="col-md-1">
                        {/* <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}> */}
                        <button
                            className={`bp3-button bp3-minimal bp3-intent-danger bp3-fill bp3-icon-delete`}
                            style={{ height: '100%' }}
                            onClick={this.props.onRemove}
                        >
                            {/* Remove */}
                        </button>
                        {/* </div> */}
                    </div>

                    <div className="col-md-6">
                        {frag.ranges.map((range, rangeIndex) => {
                            return (
                                // i wrote it, but no idea how this works
                                <CellFragmentRange
                                    key={rangeIndex}
                                    from={range[0]} to={range[1]}
                                    onStartChange={newValue => this.props.onRangeChange(rangeIndex, 0, newValue)}
                                    onEndChange={newValue => this.props.onRangeChange(rangeIndex, 1, newValue)}
                                />
                            );
                        })}
                        {this.props.shouldAddRange() && (
                            <button
                                className="bp3-button bp3-outlined bp3-intent-primary bp3-icon-add"
                                onClick={this.props.onAddRange}
                            >
                                Add Range
                            </button>
                        )}
                    </div>

                    <div className="col-md-5">
                        <label className="bp3-label">
                            Faculty
                            <div className="bp3-select bp3-fill">
                                <FacultyInput
                                    value={frag.facultyId}
                                    onChange={e => this.props.onFacultyChange(e.target.value)}
                                />
                            </div>
                        </label>

                        <label className="bp3-label">
                            Subject
                            <div className="bp3-select bp3-fill">
                                <SubjectInput
                                    value={frag.subjectId}
                                    facultyId={frag.facultyId}
                                    onChange={e => this.props.onSubjectChange(e.target.value)}
                                />
                            </div>
                        </label>

                    </div>


                </div>
            </div>
        );
    }
}


function getEmptyFragment() {
    const faculty = window.facultyData.length > 0 ? window.facultyData[0] : {};
    return {
        ranges: [[1, 6]],
        facultyId: faculty.id,
        subjectId: faculty.allowedSubjects[0],
    };
}

function getLectureName(type, index) {

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

    // if (type == 1) {
    // return "Break";
    // }
    // return `Lecture ${index + 1}`;
}

window.getLectureName = getLectureName;

class CellDialoge extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            fragments: [],
            fragmentsActiveStatus: [],
            activeCellData: {
                lectureName: "",
                sectionName: ""
            }
        }
    }

    _isActiveCellEqual(cell1, cell2) {
        return cell1.sectionId == cell2.sectionId && cell1.lectureIndex == cell2.lectureIndex;
    }

    ExtractCellData(sectionId, lectureIndex) {
        const tableData = window.tableData;

        const result = {
            fragments: [],
            sectionName: '',
            lectureName: getLectureName(window.tableData.lectures[lectureIndex], lectureIndex)
        }


        for (let i = 0; i < tableData.sections.length; i++) {
            const section = tableData.sections[i];
            if (section.id == sectionId) {
                result.sectionName = section.name;

                for (let j = 0; j < section.cells.length; j++) {
                    const cell = section.cells[j];
                    if (cell.lectureIndex == lectureIndex) {
                        // return {
                        //     fragments: JSON.parse(JSON.stringify(cell.fragments)),
                        //     sectionName: section.name
                        // };

                        // deep copy
                        result.fragments = JSON.parse(JSON.stringify(cell.fragments));
                        return result;

                    }
                }
                return result;
            }
        }

        return result;

    }

    componentDidUpdate(prevProps) {

        const activeCell = this.props.activeCell;

        if (!this._isActiveCellEqual(activeCell, prevProps.activeCell)) {

            const cellData = this.ExtractCellData(
                this.props.activeCell.sectionId,
                this.props.activeCell.lectureIndex,
            );

            const fragments = cellData.fragments;

            let fragmentsActiveStatus = [];

            for (let i = 0; i < fragments.length; i++) {
                // fragments[i].active = true;
                fragmentsActiveStatus.push(true);
            }

            this.setState({
                fragments, fragmentsActiveStatus,
                activeCellData: {
                    lectureName: cellData.lectureName,
                    sectionName: cellData.sectionName
                }
            });

        }
    }

    addFragment = () => {
        this.setState({
            fragments: [...this.state.fragments, getEmptyFragment()],
            fragmentsActiveStatus: [...this.state.fragmentsActiveStatus, true],
        });
    };


    handleAddRange = (fragmentIndex) => {
        let fragments = [...this.state.fragments];
        let fragment = { ...fragments[fragmentIndex] };

        fragment.ranges = [...fragment.ranges, [1, 1]];
        fragments[fragmentIndex] = fragment;
        this.setState({ fragments });
    };

    handleRangeChange = (fragmentIndex, rangeIndex, elemIndex, rangeValue) => {
        let fragments = [...this.state.fragments];
        let fragment = { ...fragments[fragmentIndex] };
        let ranges = [...fragment.ranges];

        let range = ranges[rangeIndex];
        range[elemIndex] = parseInt(rangeValue);

        fragment.ranges[rangeIndex] = range;
        fragments[fragmentIndex] = fragment;


        this.setState({ fragments });
    };


    shouldAddRange = (fragmentIndex) => {
        const fragment = this.state.fragments[fragmentIndex];

        return fragment && fragment.ranges.length < 6;

        // return this.state.fragments[fragmentIndex].ranges.length < 6;
    };

    handleFacultyChange = (fragmentIndex, facultyId) => {
        let fragments = [...this.state.fragments];
        let fragment = { ...fragments[fragmentIndex], facultyId: parseInt(facultyId) };
        fragments[fragmentIndex] = fragment;
        this.setState({ fragments });
    };

    handleSubjectChange = (fragmentIndex, subjectId) => {
        let fragments = [...this.state.fragments];
        let fragment = { ...fragments[fragmentIndex], subjectId: parseInt(subjectId) };
        fragments[fragmentIndex] = fragment;
        this.setState({ fragments });
    };

    onRemove = (fragmentIndex) => {
        let fragmentsActiveStatus = [...this.state.fragmentsActiveStatus];
        fragmentsActiveStatus[fragmentIndex] = false;
        this.setState({ fragmentsActiveStatus });
    };

    getModelTitle() {
        // return `Edit Cell (${this.state.activeCellData.lectureName}`
        return (
            <span>
                Edit Cell

                <small className="ml-tag">
                    ({this.state.activeCellData.sectionName} - {this.state.activeCellData.lectureName})
                </small>
            </span>
        );
    }


    render() {
        return (
            <Dialog
                style={{
                    width: '70vw'
                }}

                icon="flow-branch"
                transitionDuration={0}

                onClose={this.props.onClose}
                title={this.getModelTitle()}
                autoFocus={true}
                canEscapeKeyClose={true}
                canOutsideClickClose={false}
                enforceFocus={true}
                usePortal={true}
                isOpen={this.props.open}
            >
                <div className="bp3-dialog-body">

                    {this.state.fragments.map((frag, i) => {
                        if (!this.state.fragmentsActiveStatus[i]) {
                            return false;
                        }
                        return (
                            <React.Fragment key={i}>
                                <h6 className="bp3-heading mb-sm">Range:</h6>
                                <CellFragment
                                    data={frag}

                                    onFacultyChange={this.handleFacultyChange.bind(this, i)}
                                    onSubjectChange={this.handleSubjectChange.bind(this, i)}
                                    onRangeChange={this.handleRangeChange.bind(this, i)}
                                    shouldAddRange={this.shouldAddRange.bind(this, i)}
                                    onAddRange={this.handleAddRange.bind(this, i)}
                                    onRemove={this.onRemove.bind(this, i)}
                                />
                                <br />
                            </React.Fragment>
                        );
                    })}


                    {this.state.fragments.length < 6 && (

                        <button
                            className="bp3-button bp3-fill bp3-outlined bp3-intent-warning bp3-icon-add"
                            onClick={this.addFragment}
                        >
                            Add Segment
                        </button>
                    )}


                </div>
                {this.renderFooter()}
            </Dialog>
        );
    }


    GetFragmentsPayload = () => {
        // return this.state.fragments.map((frag, index) => {
        //     return this.state.fragmentsActiveStatus[index] && frag;
        // }).filter(Boolean);

        let fragments = [];
        for (let i = 0; i < this.state.fragments.length; i++) {
            if (this.state.fragmentsActiveStatus[i]) {
                fragments.push(this.state.fragments[i]);
            }
        }

        return fragments;
    };

    handleSave = () => {
        // console.log(this.state.fragments);

        redirectUrl(window.SERVER_DATA.urls.update_cell, {
            csrfmiddlewaretoken: window.TOKEN,
            fragments_json: JSON.stringify(this.GetFragmentsPayload()),
            table_id: window.SERVER_DATA.table_id,
            college_id: window.SERVER_DATA.college.id,

            lecture_index: this.props.activeCell.lectureIndex,
            section_id: this.props.activeCell.sectionId

        }, 'post');

    };


    renderFooter() {
        return (
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
                        onClick={this.handleSave}

                    >
                        <span className="bp3-button-text">Save Cell</span>
                    </button>

                </div>
            </div>
        );
    }

}

export default CellDialoge;