import { useState } from 'react';
import './Input.css';

const Input = ({
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  helperText,
  required = false,
  disabled = false,
  leftIcon,
  rightIcon,
  className = '',
  ...props
}) => {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <div className={`input-wrapper ${className}`}>
      {label && (
        <label className="input-label">
          {label}
          {required && <span className="input-required">*</span>}
        </label>
      )}
      
      <div className={`input-container ${isFocused ? 'focused' : ''} ${error ? 'error' : ''}`}>
        {leftIcon && <span className="input-icon input-icon-left">{leftIcon}</span>}
        
        <input
          type={type}
          className="input-field"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          disabled={disabled}
          required={required}
          {...props}
        />
        
        {rightIcon && <span className="input-icon input-icon-right">{rightIcon}</span>}
      </div>
      
      {(error || helperText) && (
        <span className={`input-helper ${error ? 'input-error' : ''}`}>
          {error || helperText}
        </span>
      )}
    </div>
  );
};

export default Input;
