import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';
import "flatpickr/dist/themes/light.css";


import AtndSheetForm from './atndsheet';
import LectureSheetForm from './lecsheet';


function GenerateReportsApp() {
    // return <AtndSheetForm />


    return (
        <React.Fragment>
            <div className="row rp-form-row">
                <div className="col-md-4 rp-form-col">
                    <h6 className="bp3-heading">Attendance Sheet</h6>

                    <AtndSheetForm />
                </div>

                <div className="col-md-4 rp-form-col">
                    <h6 className="bp3-heading">Lecture Sheet</h6>

                    <LectureSheetForm />
                </div>

            </div>
        </React.Fragment>
    );

}


ReactDOM.render(
    <GenerateReportsApp />,
    document.getElementById('root')
);
