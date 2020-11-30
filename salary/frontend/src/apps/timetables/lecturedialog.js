import React from 'react';

import { Dialog } from '@blueprintjs/core/lib/esm/components/dialog/dialog';

class LectureDialog extends React.Component {

    constructor(props) {
        super(props)

        this.state = {

        };
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
                title="Edit Lectures"
                autoFocus={true}
                canEscapeKeyClose={true}
                canOutsideClickClose={false}
                enforceFocus={true}
                usePortal={true}
                isOpen={this.props.open}
            >
                <div className="bp3-dialog-body">
                    <div className="row row-sm">
                        <div className="col-md-4">
                            <span class="bp3-tag bp3-fill bp3-large bp3-minimal bp3-intent-danger">
                                <strong style={{ margin: 'auto' }}>Lecture 1</strong>
                            </span>
                        </div>
                    </div>
                </div>
            </Dialog>
        );
    }
}

export default LectureDialog;



