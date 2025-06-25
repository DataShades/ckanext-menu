ckan.module('menu-sortable-menu-items', function ($) {
  return {
    options: {
      prefix: '',
      target: null
    },
    initialize: function () {
        $.proxyAll(this, /_on/);

        var _this = this;
        var _this_element = _this.el[0];
        function initSortable(container) {
            Sortable.create(container, {
                group: 'nested',
                handle: '.drag-handle',
                animation: 150,
                fallbackOnBody: true,
                swapThreshold: 0.65,
                ghostClass: 'ghost',
                onAdd: () => initNestedLists(),  // re-init newly added nested ULs
            });

            // Recurse through children
            Array.from(container.children).forEach(li => {
            const childUl = li.querySelector('ul');
            if (childUl) {
                initSortable(childUl);
            }
            });
        }

        function initNestedLists() {
            if (!_this_element.hasAttribute('data-sortable-initialized')) {
                initSortable(_this_element);
                _this_element.setAttribute('data-sortable-initialized', 'true');
            }
        }

        function serializeList(list, parentId = null) {
            const items = [];
            let order = 0;
            list.querySelectorAll(':scope > li').forEach(li => {
            const id = parseInt(li.dataset.id);
            items.push({ id: id, pid: parentId, order: order++ });

            const childUl = li.querySelector('ul');
            if (childUl) {
                items.push(...serializeList(childUl, id));
            }
            });
            return items;
        }

        $('#store-menu-order').on('click', () => {
            const menu = _this_element;
            const data = serializeList(menu);
            const client = _this.sandbox.client;
            client.call('POST', "menu_items_update_order", {"data": data}, _this._onUpdatedOrder);
        });

        // Initialize sortable tree on load
        initNestedLists();
    },
    _onUpdatedOrder: function(json) {
        if (json.success) {
            location.reload();
        } else {
            console.log(json.error);
        }
    }
  };
});
