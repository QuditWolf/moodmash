import { useState, useRef } from 'react';
import { Upload, X, File } from 'lucide-react';
import './FileUpload.css';

const FileUpload = ({
  accept = '*',
  multiple = false,
  maxSize = 10 * 1024 * 1024, // 10MB default
  onUpload,
  label = 'Upload files',
  helperText,
}) => {
  const [files, setFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    handleFiles(droppedFiles);
  };

  const handleChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    handleFiles(selectedFiles);
  };

  const handleFiles = (newFiles) => {
    const validFiles = newFiles.filter(file => {
      if (file.size > maxSize) {
        alert(`${file.name} is too large. Max size is ${maxSize / 1024 / 1024}MB`);
        return false;
      }
      return true;
    });

    const updatedFiles = multiple ? [...files, ...validFiles] : validFiles;
    setFiles(updatedFiles);
    
    if (onUpload) {
      onUpload(updatedFiles);
    }
  };

  const removeFile = (index) => {
    const updatedFiles = files.filter((_, i) => i !== index);
    setFiles(updatedFiles);
    if (onUpload) {
      onUpload(updatedFiles);
    }
  };

  const handleClick = () => {
    inputRef.current?.click();
  };

  return (
    <div className="file-upload">
      {label && <label className="file-upload-label">{label}</label>}
      
      <div
        className={`file-upload-dropzone ${dragActive ? 'active' : ''}`}
        onClick={handleClick}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <Upload size={32} className="file-upload-icon" />
        <p className="file-upload-text">
          <strong>Click to upload</strong> or drag and drop
        </p>
        {helperText && <p className="file-upload-helper">{helperText}</p>}
        
        <input
          ref={inputRef}
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={handleChange}
          className="file-upload-input"
        />
      </div>

      {files.length > 0 && (
        <div className="file-upload-list">
          {files.map((file, index) => (
            <div key={index} className="file-upload-item">
              <File size={16} />
              <span className="file-upload-name">{file.name}</span>
              <span className="file-upload-size">
                {(file.size / 1024).toFixed(1)} KB
              </span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile(index);
                }}
                className="file-upload-remove"
              >
                <X size={16} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
