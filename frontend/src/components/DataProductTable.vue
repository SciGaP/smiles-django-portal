<template>
  <b-container fluid>
    <b-row class="m-2 mb-4">
      <b-col lg="5" class="my-2">
        <b-form-group
            label="Filter"
            label-for="filter-input"
            label-cols-sm="3"
            label-align-sm="right"
            label-size="sm"
            class="mb-0"
        >
          <b-input-group size="sm">
            <b-form-input
                id="filter-input"
                v-model="filter"
                type="search"
                placeholder="Type to Search"
            ></b-form-input>

            <b-input-group-append>
              <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form-group>
      </b-col>
    </b-row>

    <b-table
        responsive
        :items="items"
        :fields="fields"
        :current-page="currentPage"
        :per-page="perPage"
        :filter="filter"
        stacked="md"
        show-empty
        small
        @filtered="onFiltered"
    >
      <template #cell(actions)="row">
        <div class="text-right">
          <b-button size="sm" @click="row.toggleDetails">
            {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
          </b-button>
          <b-button size="sm" variant="primary" class="m-1" @click="edit(row.item)">
            Edit
          </b-button>
          <b-button size="sm" variant="danger" @click="deleteRecord(row)">
            Delete
          </b-button>
        </div>

      </template>

      <template #row-details="row">
        <b-card>
          <ul>
            <li v-for="(value, key) in row.item" :key="key">
              <b>{{ key }}:</b> {{ value }}
            </li>
          </ul>
        </b-card>
      </template>
    </b-table>

    <b-row class="mb-4">
      <b-col sm="7" md="3" class="my-1">
        <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            align="fill"
            size="sm"
            class="my-0"
        ></b-pagination>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import {smilesDPService} from "@/services/smiles-dp-service";

export default {
  name: "SMILESDataProductTable",
  data() {
    return {
      items: [],
      totalRows: 1,
      currentPage: 1,
      perPage: 15,
      filter: null,
      type: this.$route.query.type
    }
  },
  computed: {
    fields() {
      return smilesDPService.getDisplayableColumns(this.type);
    }
  },
  mounted() {
    this.loadSMILESDataProducts();
  },
  methods: {
    loadSMILESDataProducts() {
      this.isLoading = true;
      this.params = `type=${this.type}&page=${this.currentPage}&size=${this.perPage}`;
      smilesDPService.getSMILESDataProducts(this.params).then((response) => {
        if (response.data) {
          this.items = response.data;
          // Set the initial number of items
          this.totalRows = this.items.length
        }
      });
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
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
            console.log(data.item.data_product_id)
            if (value) {
              //TODO - this 'type' should extracted from the SMILES DP
              smilesDPService.deleteSMILESDataProduct(this.type, data.item.data_product_id)
              const index = this.items.findIndex(item => item.data_product_id === data.item.data_product_id);
              if (index !== -1) {
                this.items.splice(index, 1);
              }
            }
          });
    },
    edit(data) {
      alert(JSON.stringify(data));
    }
  }
}
</script>