<template>
  <div id="app">
    <div class="container mt-5" style="overflow-x: auto;">
      <div class="card">
        <div class="card-body">
          <b-table
              responsive
              class="table table-striped table-hover"
              :items="listItems"
              :fields="fields"
              :current-page="currentPage"
              :per-page="0"
          >
            <template v-slot:cell(action)="data">
              <div class="btn-group" role="group">
                <b-button size="sm" variant="primary" class="mr-1" @click="edit(data)">
                  Edit
                </b-button>
                <b-button size="sm" variant="danger" @click="deleteRecord(data)">
                  Delete
                </b-button>
              </div>
            </template>
          </b-table>
          <b-pagination
              v-model="currentPage"
              :total-rows="totalPages"
              :per-page="recordsPerPage"
              class="my-3"
          ></b-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {smilesDPService} from "@/services/smiles-dp-service";

export default {
  name: "SMILESDataProductTable",
  data() {
    return {
      listItems: [],
      currentPage: 1,
      totalPages: 0,
      recordsPerPage: 20,
      isLoading: false,
      fields: ["name", "mol_id", "cas_nr", "smiles", "smiles_stereo", "inchi", "emp_formula", "emp_formula_source",
        "mw", "mw_source", "journal", "year_publ",
        "action"],
      params: "",
    };
  },
  created() {
    this.loadSMILESDataProducts();
  },
  watch: {
    currentPage: {
      handler: function (value) {
        this.params = `page=${value}&size=${this.recordsPerPage}`;
        this.loadSMILESDataProducts();
      },
    },
  },
  methods: {
    loadSMILESDataProducts() {
      this.isLoading = true;
      this.params = `page=${this.currentPage}&size=${this.recordsPerPage}`;
      smilesDPService.getSMILESDataProducts(this.params).then((response) => {
        if (response.data) {
          this.listItems = response.data;
          this.totalPages = 40;
          this.isLoading = false;
        }
      });
    },
    deleteRecord(data) {
      this.$bvModal
          .msgBoxConfirm("Do you want to delete the record?", {
            title: "Record Delete Confirmation",
            size: "mm",
            buttonSize: "sm",
            okVariant: "danger",
            okTitle: "YES",
            cancelTitle: "NO",
            footerClass: "p-2",
            hideHeaderClose: false,
            centered: true,
          })
          .then((value) => {
            if (value) {
              this.listItems.splice(data.index, 1);
            }
          });
    },
    edit(data) {
      alert(JSON.stringify(data));
    },
  },
};
</script>

<style scoped>
.table-action-btns > button {
  margin-right: 0.5rem;
}

.pagination > li > a,
.pagination > li > span {
  color: #007bff;
  margin: 0 0.2rem;
  border-radius: 0.25rem;
  padding: 0.5rem 0.75rem;
  text-decoration: none;
  border: 1px solid #007bff;
}

.pagination > .active > a,
.pagination > .active > span {
  background-color: #007bff;
  color: #fff;
  border: 1px solid #007bff;
}

.pagination > .disabled > span,
.pagination > .disabled > a,
.pagination > .disabled > a:hover,
.pagination > .disabled > a:focus {
  color: #6c757d;
  pointer-events: none;
  background-color: #fff;
  border-color: #6c757d;
}

.pagination > li:first-child > a,
.pagination > li:first-child > span {
  border-top-left-radius: 0.25rem;
  border-bottom-left-radius: 0.25rem;
}

.pagination > li:last-child > a,
.pagination > li:last-child > span {
  border-top-right-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}
</style>
