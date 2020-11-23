import React from 'react';

import Flatpickr from "react-flatpickr";


// function DateInput({ value, onChange, serverName, placeholder = "Select Date" }) {
//     return <Flatpickr
//         value={value}
//         onChange={onChange}
//         className="form-control"
//         options={{
//             altInput: true,
//             altFormat: "F j, Y",
//             dateFormat: "Y-m-d",
//             allowInput: true

//         }}
//         render={({ defaultValue, value, ...props }, ref) => {
//             return <input
//                 {...props}
//                 defaultValue={defaultValue}
//                 ref={ref}
//                 placeholder={placeholder}
//                 name={serverName}
//             />;
//         }}

//     />;
// }

function DateInput({ icon = undefined, value, onChange, serverName, placeholder = "Select Date" }) {
    return <Flatpickr
        value={value}
        onChange={onChange}
        // className="form-control"
        options={{
            altInput: true,
            altFormat: "F j, Y",
            dateFormat: "Y-m-d",
            allowInput: true

        }}
        render={({ defaultValue, value, ...props }, ref) => {
            return <input
                {...props}
                defaultValue={defaultValue}
                className="bp3-input bp3-fill no-intent"
                ref={ref}
                placeholder={placeholder}
                name={serverName}
            />;
        }}
    />;
}

export default DateInput;
