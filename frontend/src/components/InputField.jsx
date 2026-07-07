function InputField({ label, children }) {
  return (
    <div className="input-field">
      <label>{label}</label>
      {children}
    </div>
  );
}

export default InputField;