<template>
  <div class="file-upload">
    <label class="file-upload__label" :class="{'file-upload__label--has-file': file, 'no-click': uploading}">
      <span class="file-upload__text">{{ file ? file.name : 'Drag and drop or click to select a file' }}</span>
      <input class="file-upload__input" type="file" @change="onFileSelected" ref="fileInput"/>
    </label>
    <div class="upload-container">
      <div class="add-to-container">
        <span class="add-to-label">Add to</span>
      </div>
      <div class="upload-checkboxes" :class="{ 'no-click': uploading}">
        <label>
          <input type="radio" v-model="selectedDatabase" value="Literature Database">
          <span class="checkbox-label" :class="{ 'checkbox-selected': selectedDatabase === 'Literature Database' }">Literature Database</span>
        </label>
        <label>
          <input type="radio" v-model="selectedDatabase" value="Computational Database">
          <span class="checkbox-label" :class="{ 'checkbox-selected': selectedDatabase === 'Computational Database' }">Computational Database</span>
        </label>
        <label>
          <input type="radio" v-model="selectedDatabase" value="Experimental Database">
          <span class="checkbox-label" :class="{ 'checkbox-selected': selectedDatabase === 'Experimental Database' }">Experimental Database</span>
        </label>
      </div>
      <div class="upload-buttons">
        <button class="file-upload__button" :disabled="!file" :class="{'file-upload__button--disabled': uploading}"
                @click="uploadFile">
          <span v-if="!uploading">Upload a file</span>
          <span v-else>Uploading...</span>
        </button>
        <button class="form-upload__button" :class="{'form-upload__button--active': formOpen}"
                @click="formOpen = !formOpen">Fill up a form
        </button>
      </div>
      <div class="progress-bar-container" v-if="progress !== 0">
        <div class="file-upload__progress" v-if="uploading">
          <div class="file-upload__progress-bar" :style="{ width: progress + '%' }"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "FileUpload",

  data() {
    return {
      file: null,
      uploading: false,
      // uploadProgress: null,
      selectedDatabase: 'Computational Database',
      formOpen: false,
      progress: 0
    };
  },

  computed: {
    uploadUrl() {
      const URL_PREFIX = 'http://127.0.0.1:8000/smiles/';
      if (this.selectedDatabase === 'Literature Database') {
        return URL_PREFIX + 'literature-dp/upload';
      } else if (this.selectedDatabase === 'Experimental Database') {
        return URL_PREFIX + 'experimental-dp/upload';
      } else if (this.selectedDatabase === 'Computational Database') {
        return URL_PREFIX + 'computational-dp/upload';
      } else {
        return '';
      }
    }
  },

  methods: {
    onFileSelected(e) {
      this.file = e.target.files[0];
    },
    uploadFile() {
      if (!this.uploading && this.file) {
        this.uploading = true;
        const formData = new FormData();
        formData.append("file", this.file);
        axios
            .post(this.uploadUrl, formData, {
              onUploadProgress: (progressEvent) => {
                this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              }
            })
            .then(response => {
              this.uploading = false;
              this.progress = 0;
              this.file = null;
              this.$refs.fileInput.value = '';
              alert("File upload successful!");
              console.log(response)
            })
            .catch(error => {
              console.log(error);
              this.uploading = false;
              this.progress = 0;
              this.file = null;
              this.$refs.fileInput.value = '';
            });
      }
    }
  }
};
</script>

<style scoped>

.file-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 600px;
  padding: 20px;
}

.file-upload__label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  font-size: 20px;
  color: #777;
  text-align: center;
  padding: 10px;
  border: 2px dashed #ccc;
  border-radius: 10px;
  height: 60px;
  margin-bottom: 20px;
}

.file-upload__label:hover,
.file-upload__label--has-file {
  background-color: #f8f8f8;
}

.file-upload__input {
  display: none;
}

.file-upload__text {
  margin-top: 10px;
  margin-bottom: 10px;
}

.file-upload__button {
  background-color: #fff;
  color: #333;
  border: 2px solid #333;
  border-radius: 5px;
  padding: 10px;
  margin-right: 10px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.file-upload__button:hover:not(.file-upload__button--disabled) {
  background-color: #333;
  color: #fff;
}

.file-upload__button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-upload__button {
  background-color: #fff;
  color: #333;
  border: 2px solid #333;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.form-upload__button:hover:not(.form-upload__button--active) {
  background-color: #333;
  color: #fff;
}

.form-upload__button--active {
  background-color: #333;
  color: #fff;
}

.upload-checkboxes {
  display: flex;
  flex-direction: row;
  margin-bottom: 20px;
}

.upload-checkboxes label {
  display: flex;
  flex-direction: row;
  margin-right: 10px;
}

.upload-checkboxes input[type="checkbox"] {
  margin-right: 5px;
}

.progress-bar-container {
  margin-top: 20px;
  width: 100%;
}

.file-upload__progress {
  background-color: #ccc;
  border-radius: 10px;
  height: 10px;
  width: 100%;
  overflow: hidden;
}

.file-upload__progress-bar {
  height: 100%;
  background-color: #333;
  transition: width 0.2s ease-in-out;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  margin-right: 25px;
  padding: 8px;
  border-radius: 8px;
  background-color: #f5f5f5;
  color: #333;
  cursor: pointer;
}

.checkbox-label:hover {
  background-color: #ebebeb;
}

input[type="radio"] {
  display: none;
}

input[type="radio"] + .checkbox-label::before {
  content: "";
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 10px;
  border-radius: 3px;
  border: 1px solid #ccc;
  vertical-align: middle;
}

input[type="radio"]:checked + .checkbox-label::before {
  background-color: #333;
  border-color: #333;
}

.upload-container {
  text-align: center;
  margin-top: 40px;
  height: 50%;
}

.add-to-container {
  margin-bottom: 16px;
}

.add-to-label {
  font-size: 24px;
  font-weight: bold;
}

.upload-buttons {
  margin-top: 80px;
}

.no-click {
  pointer-events: none;
}

</style>